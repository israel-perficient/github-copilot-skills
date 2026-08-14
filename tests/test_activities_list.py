"""
Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern.

This module tests the activities listing functionality, ensuring the API
returns the correct structure and data for all available activities.
"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint."""
    
    def test_returns_all_activities(self, client, fresh_activities):
        """
        Test that GET /activities returns all activities in the database.
        
        AAA Pattern:
        - Arrange: Set up fresh activities database (via fixture)
        - Act: Make GET request to /activities endpoint
        - Assert: Verify response contains all 9 activities
        """
        # Arrange
        expected_activity_count = 9
        expected_activities = {
            "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
            "Soccer Club", "Art Studio", "Drama Club", "Debate Team", "Science Club"
        }
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert len(data) == expected_activity_count
        assert set(data.keys()) == expected_activities
    
    def test_activity_has_required_fields(self, client, fresh_activities):
        """
        Test that each activity contains required fields with correct types.
        
        AAA Pattern:
        - Arrange: Define required fields and their expected types
        - Act: Fetch activities and inspect first activity
        - Assert: Verify all required fields exist and have correct structure
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Get first activity
        first_activity_name = list(activities.keys())[0]
        first_activity = activities[first_activity_name]
        
        # Assert
        assert all(field in first_activity for field in required_fields)
        assert isinstance(first_activity["description"], str)
        assert isinstance(first_activity["schedule"], str)
        assert isinstance(first_activity["max_participants"], int)
        assert isinstance(first_activity["participants"], list)
    
    def test_participants_list_is_populated(self, client, fresh_activities):
        """
        Test that activities have participant data populated.
        
        AAA Pattern:
        - Arrange: Identify activities with expected participants
        - Act: Fetch activities from API
        - Assert: Verify participant lists contain email addresses
        """
        # Arrange
        activity_with_participants = "Chess Club"
        expected_min_participants = 1  # Each activity should have at least some participants
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        participants = activities[activity_with_participants]["participants"]
        
        # Assert
        assert len(participants) >= expected_min_participants
        assert all(isinstance(email, str) and "@" in email for email in participants)
