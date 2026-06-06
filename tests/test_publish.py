import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from blog.models import Post


@pytest.mark.django_db
class TestPublishPost:
    """Publishing a draft makes it visible to the public."""

    def test_published_post_appears_on_homepage(self, client):
        """After publishing, the post is visible on the public homepage."""
        # Arrange: Create a published post via admin
        user = User.objects.create_user(username="author", password="testpass123")

        # First, authenticate and login via 2FA (simplified - use force_login)
        client.force_login(user)

        # Publish a post
        client.post("/admin/new-post/", {
            "title": "Freshly Published",
            "content": "This is new content",
            "publish": "Publish",
        })

        # Act: Visit the public homepage (not logged in)
        # First logout to simulate public visitor
        client.post("/logout/")

        response = client.get("/")

        # Assert: Published post appears on homepage
        assert response.status_code == 200
        content = response.content.decode()
        assert "Freshly Published" in content

    def test_draft_post_does_not_appear_on_homepage(self, client):
        """Draft posts are not visible to the public."""
        # Arrange: Create a draft post
        user = User.objects.create_user(username="author", password="testpass123")
        client.force_login(user)

        client.post("/admin/new-post/", {
            "title": "Secret Draft",
            "content": "Not ready yet",
            "save_as_draft": "Save as Draft",
        })

        # Act: Logout and visit homepage as public visitor
        client.post("/logout/")
        response = client.get("/")

        # Assert: Draft post does NOT appear
        assert response.status_code == 200
        content = response.content.decode()
        assert "Secret Draft" not in content
