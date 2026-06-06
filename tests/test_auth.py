import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestLoginPage:
    """The login page allows authors to authenticate."""

    def test_login_page_has_form_with_csrf_token(self, client):
        """The login page includes a form with CSRF protection."""
        response = client.get("/login/")

        assert response.status_code == 200
        content = response.content.decode()

        # Form elements present
        assert 'name="username"' in content
        assert 'name="password"' in content
        # CSRF token is present
        assert 'csrfmiddlewaretoken' in content

    def test_valid_credentials_redirect_to_2fa(self, client):
        """Submitting valid credentials redirects to 2FA page."""
        # Arrange: Create a user
        User.objects.create_user(username="author", password="testpass123")

        # Act: Submit login form
        response = client.post("/login/", {
            "username": "author",
            "password": "testpass123",
        })

        # Assert: Should redirect to 2FA page
        assert response.status_code == 302  # Redirect
        assert response.url == "/2fa/"

    def test_invalid_credentials_show_error(self, client):
        """Submitting invalid credentials shows error message."""
        # Arrange: Create a user
        User.objects.create_user(username="author", password="testpass123")

        # Act: Submit login form with wrong password
        response = client.post("/login/", {
            "username": "author",
            "password": "wrongpassword",
        })

        # Assert: Should stay on login page with error
        assert response.status_code == 200
        assert "error" in response.content.decode().lower() or "invalid" in response.content.decode().lower()
