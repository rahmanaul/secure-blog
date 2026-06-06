import pytest
from django.utils import timezone
from blog.models import Post


@pytest.mark.django_db
class TestHomepageListsPublishedPosts:
    """A visitor sees a list of published blog posts on the homepage."""

    def test_published_post_appears_on_homepage(self, client):
        """Given a published post, it appears on the homepage with title and date."""
        # Arrange: Create a published post
        post = Post.objects.create(
            title="Security First: A Case Study",
            content="This is a post about security...",
            published_at=timezone.now(),
        )

        # Act: Visit the homepage
        response = client.get("/")

        # Assert: Post is visible
        assert response.status_code == 200
        assert "Security First: A Case Study" in response.content.decode()
        # The date should be displayed
        assert post.published_at.strftime("%Y-%m-%d") in response.content.decode()

    def test_draft_post_does_not_appear_on_homepage(self, client):
        """Given a draft post, it does NOT appear on the homepage."""
        # Arrange: Create a draft post (no published_at)
        Post.objects.create(
            title="Draft: Half-Baked Ideas",
            content="This is still being written...",
            # published_at is None = draft
        )

        # Act: Visit the homepage
        response = client.get("/")

        # Assert: Draft post is NOT visible
        assert response.status_code == 200
        assert "Half-Baked Ideas" not in response.content.decode()
        assert "Draft:" not in response.content.decode()
