"""
Shared test fixtures and configuration for the FastAPI test suite.

This module provides:
- FastAPI TestClient connected to the application
- Fresh activity database fixture for test isolation
- Common test data fixtures
"""

import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provide a TestClient connected to the FastAPI application.
    
    Yields:
        TestClient: FastAPI test client for making requests to endpoints
    """
    # Arrange: Create client
    yield TestClient(app)


@pytest.fixture
def fresh_activities():
    """
    Provide a fresh copy of the activities database for each test.
    
    This fixture ensures test isolation by providing a deep copy of the
    original activities dictionary, preventing tests from affecting each other.
    
    Yields:
        dict: Fresh copy of activities database
    """
    # Arrange: Create a deep copy of the original activities
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for varsity and recreational players",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Soccer Club": {
            "description": "Join us for soccer matches and skill development",
            "schedule": "Wednesdays and Saturdays, 3:00 PM - 4:30 PM",
            "max_participants": 22,
            "participants": ["lucas@mergington.edu", "maya@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media techniques",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["grace@mergington.edu"]
        },
        "Drama Club": {
            "description": "Act in plays, musicals, and theatrical performances",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["james@mergington.edu", "isabella@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop critical thinking and public speaking skills through debate",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["ethan@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["ava@mergington.edu", "noah@mergington.edu"]
        }
    }
    
    # Store original state
    test_activities = deepcopy(original_activities)
    
    # Replace app's activities with test copy
    activities.clear()
    activities.update(test_activities)
    
    yield activities
    
    # Cleanup: Restore original activities after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def empty_activity_db():
    """
    Provide an empty activities database for tests that need a clean slate.
    
    Yields:
        dict: Empty activities database
    """
    # Arrange: Clear and store original state
    original_activities = deepcopy(activities)
    activities.clear()
    
    yield activities
    
    # Cleanup: Restore original activities
    activities.clear()
    activities.update(original_activities)
