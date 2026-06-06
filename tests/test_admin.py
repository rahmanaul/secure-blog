import pytest
from django.contrib.auth.models import User
from blog.models import Post


@pytest.mark.django_db
class TestAdminDashboard:
    """Authenticated authors can access the admin dashboard."""

    def test_authenticated_user_sees_new_post_link(self, client):
        """Logged-in users see the New Post option."""
        # Arrange: Create and login a user
        user = User.objects.create_user(username="author", password="testpass123")
        client.force_login(user)

        # Act: Visit admin dashboard
        response = client.get("/admin/")

        # Assert: New Post link is present
        assert response.status_code == 200
        content = response.content.decode()
        assert "New Post" in content
        assert "/admin/new-post/" in content

    def test_unauthenticated_user_redirected_to_login(self, client):
        """Users not logged in are redirected to login."""
        # Act: Visit admin dashboard without logging in
        response = client.get("/admin/")

        # Assert: Redirected to login
        assert response.status_code == 302
        assert "/login/" in response.url
