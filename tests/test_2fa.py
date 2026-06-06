import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestTwoFactorAuth:
    """Email 2FA completes the authentication flow."""

    def test_2fa_page_requires_login_first(self, client):
        """The 2FA page is only accessible after valid credentials."""
        response = client.get("/2fa/")

        # Should redirect to login if not authenticated
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_valid_2fa_code_logs_user_in(self, client):
        """Entering correct 2FA code logs the user in."""
        # Arrange: Complete step 1 (login) and store user in session
        user = User.objects.create_user(username="author", password="testpass123")
        session = client.session
        session["auth_user_id"] = user.id
        session["2fa_code"] = "123456"  # Simulate code sent
        session.save()

        # Act: Submit 2FA form with correct code
        response = client.post("/2fa/", {"code": "123456"}, follow=True)

        # Assert: User is logged in
        assert response.status_code == 200
        # Should be able to access a protected page
        assert "_auth_user_id" in client.session
        # The original auth_user_id should be replaced with actual login
        assert client.session["_auth_user_id"] == str(user.id)

    def test_invalid_2fa_code_shows_error(self, client):
        """Entering wrong 2FA code shows error."""
        # Arrange: Complete step 1 (login) and store user in session
        user = User.objects.create_user(username="author", password="testpass123")
        session = client.session
        session["auth_user_id"] = user.id
        session["2fa_code"] = "123456"
        session.save()

        # Act: Submit 2FA form with wrong code
        response = client.post("/2fa/", {"code": "000000"})

        # Assert: Should show error
        assert response.status_code == 200
        content = response.content.decode()
        assert "error" in content.lower() or "invalid" in content.lower()
        # User should NOT be logged in
        assert "_auth_user_id" not in client.session or client.session.get("_auth_user_id") != str(user.id)
