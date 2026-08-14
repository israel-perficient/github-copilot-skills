"""
Tests for DELETE /activities/{activity_name}/unregister endpoint using AAA pattern.

This module tests student unregistration functionality, including success cases
and error handling.
"""

import pytest


class TestUnregister:
    """Test suite for DELETE /activities/{activity_name}/unregister endpoint."""
    
    def test_successful_unregister(self, client, fresh_activities):
        """
        Test successful unregister removes student from activity participants.
        
        AAA Pattern:
        - Arrange: Identify enrolled student to remove
        - Act: Make DELETE request with valid email and activity name
        - Assert: Verify student is removed and response is successful
        """
        # Arrange
        activity_name = "Chess Club"
        student_to_remove = "michael@mergington.edu"
        
        # Get initial participant count
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_to_remove}
        )
        
        # Verify participant was removed
        verification_response = client.get("/activities")
        final_count = len(verification_response.json()[activity_name]["participants"])
        final_participants = verification_response.json()[activity_name]["participants"]
        
        # Assert
        assert response.status_code == 200
        assert f"Removed {student_to_remove}" in response.json()["message"]
        assert final_count == initial_count - 1
        assert student_to_remove not in final_participants
    
    def test_unregister_nonexistent_activity_returns_404(self, client, fresh_activities):
        """
        Test that unregister fails with 404 when activity doesn't exist.
        
        AAA Pattern:
        - Arrange: Define invalid activity name
        - Act: Make DELETE request to non-existent activity
        - Assert: Verify 404 error is returned
        """
        # Arrange
        invalid_activity = "Nonexistent Club"
        student_email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{invalid_activity}/unregister",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_not_enrolled_student_returns_404(self, client, fresh_activities):
        """
        Test that unregister fails with 404 when student is not enrolled.
        
        AAA Pattern:
        - Arrange: Identify student not in activity
        - Act: Attempt to unregister student who is not enrolled
        - Assert: Verify 404 error is returned
        """
        # Arrange
        activity_name = "Chess Club"
        not_enrolled = "notenrolled@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": not_enrolled}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not signed up" in response.json()["detail"]
    
    def test_unregister_multiple_times_fails_on_second_attempt(self, client, fresh_activities):
        """
        Test that unregistering the same student twice fails on second attempt.
        
        AAA Pattern:
        - Arrange: Identify enrolled student
        - Act: Unregister once (succeeds), then attempt again (should fail)
        - Assert: Verify first succeeds (200) and second fails (404)
        """
        # Arrange
        activity_name = "Programming Class"
        student_to_remove = "emma@mergington.edu"
        
        # Act - First unregister (should succeed)
        first_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_to_remove}
        )
        
        # Act - Second unregister (should fail)
        second_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_to_remove}
        )
        
        # Assert
        assert first_response.status_code == 200
        assert second_response.status_code == 404
        assert "not signed up" in second_response.json()["detail"]
