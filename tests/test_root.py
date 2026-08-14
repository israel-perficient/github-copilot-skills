"""
Tests for GET / endpoint using AAA pattern.

This module tests the root endpoint redirect functionality.
"""

import pytest


class TestRoot:
    """Test suite for GET / endpoint."""
    
    def test_root_redirects_to_static_index(self, client):
        """
        Test that GET / redirects to /static/index.html.
        
        AAA Pattern:
        - Arrange: Prepare client
        - Act: Make GET request to root endpoint
        - Assert: Verify redirect location and status code
        """
        # Arrange
        expected_redirect_url = "/static/index.html"
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == expected_redirect_url
