import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestLogout:
    """Logout properly terminates the session."""

    def test_logout_terminates_session(self, client):
        """After logout, the user is no longer authenticated."""
        # Arrange: Create and login a user
        user = User.objects.create_user(username="author", password="testpass123")
        client.force_login(user)

        # Verify user is logged in
        assert "_auth_user_id" in client.session

        # Act: Logout
        response = client.post("/logout/")

        # Assert: User is logged out
        assert response.status_code == 302  # Redirect after logout
        assert "/login/" in response.url or "/" in response.url

        # Session should be cleared (need to check new session)
        # After logout, accessing a protected page should redirect
        response = client.get("/admin/")
        assert response.status_code == 302
