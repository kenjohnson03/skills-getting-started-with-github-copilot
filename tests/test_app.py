import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Soccer Team" in data
    assert "Basketball Club" in data


def test_signup_for_activity():
    response = client.post("/activities/Soccer%20Team/signup?email=testuser@mergington.edu")
    assert response.status_code == 200
    assert "Signed up testuser@mergington.edu for Soccer Team" in response.json()["message"]

    # Duplicate signup should fail
    response = client.post("/activities/Soccer%20Team/signup?email=testuser@mergington.edu")
    assert response.status_code == 400
    assert "Student already signed up for this activity" in response.json()["detail"]


def test_unregister_from_activity():
    # Unregister existing participant
    response = client.delete("/activities/Soccer%20Team/unregister?email=testuser@mergington.edu")
    assert response.status_code == 200
    assert "Unregistered testuser@mergington.edu from Soccer Team" in response.json()["message"]

    # Unregister non-existent participant should fail
    response = client.delete("/activities/Soccer%20Team/unregister?email=notfound@mergington.edu")
    assert response.status_code == 404
    assert "Student not registered for this activity" in response.json()["detail"]


def test_signup_invalid_activity():
    response = client.post("/activities/InvalidActivity/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_invalid_activity():
    response = client.delete("/activities/InvalidActivity/unregister?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
