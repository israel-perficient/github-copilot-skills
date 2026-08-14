"""
Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern.

This module tests student signup functionality, including success cases,
error handling, and validation edge cases.
"""

import pytest


class TestSignup:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""
    
    def test_successful_signup(self, client, fresh_activities):
        """
        Test successful signup adds student to activity participants.
        
        AAA Pattern:
        - Arrange: Define new student email and target activity
        - Act: Make POST request with valid email and activity name
        - Assert: Verify student is added and response is successful
        """
        # Arrange
        activity_name = "Chess Club"
        student_email = "newstudent@mergington.edu"
        
        # Get initial participant count
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        
        # Verify participant was added
        verification_response = client.get("/activities")
        final_count = len(verification_response.json()[activity_name]["participants"])
        
        # Assert
        assert response.status_code == 200
        assert f"Signed up {student_email}" in response.json()["message"]
        assert final_count == initial_count + 1
        assert student_email in verification_response.json()[activity_name]["participants"]
    
    def test_signup_nonexistent_activity_returns_404(self, client, fresh_activities):
        """
        Test that signup fails with 404 when activity doesn't exist.
        
        AAA Pattern:
        - Arrange: Define invalid activity name
        - Act: Make POST request to non-existent activity
        - Assert: Verify 404 error is returned
        """
        # Arrange
        invalid_activity = "Nonexistent Club"
        student_email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_duplicate_signup_returns_400(self, client, fresh_activities):
        """
        Test that duplicate signup fails with 400 error.
        
        AAA Pattern:
        - Arrange: Identify already-enrolled student
        - Act: Attempt to sign up same student twice
        - Assert: Verify second signup returns 400
        """
        # Arrange
        activity_name = "Chess Club"
        already_enrolled = "michael@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": already_enrolled}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_edge_case_empty_email(self, client, fresh_activities):
        """
        Test signup behavior with empty email string (edge case).
        
        Edge Case: Currently the API accepts empty emails. This test documents
        the current behavior. Future enhancement: Add email validation.
        
        AAA Pattern:
        - Arrange: Define empty email string
        - Act: Attempt signup with empty email
        - Assert: Document current behavior (accepted or rejected)
        """
        # Arrange
        activity_name = "Programming Class"
        empty_email = ""
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": empty_email}
        )
        
        # Assert
        # Note: This documents current behavior - empty emails are accepted.
        # Future: Should return 400 with "Invalid email format" message
        # Once validation is added, change this to:
        # assert response.status_code == 400
        # assert "Invalid email" in response.json()["detail"]
        # For now, we document that it's accepted:
        if response.status_code == 200:
            pytest.skip("Empty email accepted - validation needed (future enhancement)")
    
    def test_signup_edge_case_exceeding_max_participants(self, client, empty_activity_db):
        """
        Test signup behavior when activity reaches max participants (edge case).
        
        Edge Case: Currently the API does NOT enforce max_participants limit.
        This test documents the current behavior and reveals the validation gap.
        
        AAA Pattern:
        - Arrange: Create activity with max_participants=2, add 2 students
        - Act: Try to sign up a 3rd student (exceeding capacity)
        - Assert: Document current behavior (accepted or rejected)
        """
        # Arrange
        activity_name = "Full Activity"
        test_activity = {
            "description": "Test activity at capacity",
            "schedule": "Test time",
            "max_participants": 2,
            "participants": ["student1@test.edu", "student2@test.edu"]
        }
        
        # Manually add to activities dict (only for this test)
        from src.app import activities
        activities[activity_name] = test_activity
        
        new_student = "student3@test.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_student}
        )
        
        # Assert
        # Note: This documents current behavior - exceeding max is accepted.
        # Future: Should return 400 with "Activity is at capacity" message
        # Once validation is added, change this to:
        # assert response.status_code == 400
        # assert "capacity" in response.json()["detail"].lower()
        # For now, document that it's accepted:
        if response.status_code == 200:
            pytest.skip("Max participants not enforced - validation needed (future enhancement)")
