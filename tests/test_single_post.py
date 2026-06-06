import pytest
from django.utils import timezone
from blog.models import Post


@pytest.mark.django_db
class TestSinglePostPage:
    """A visitor can read a single published blog post."""

    def test_published_post_shows_full_content(self, client):
        """Given a published post, visiting its URL shows the full content."""
        # Arrange: Create a published post
        post = Post.objects.create(
            title="Understanding CSP",
            content="Content Security Policy is crucial for web security.\n\nIt controls what resources the browser can load.",
            published_at=timezone.now(),
        )

        # Act: Visit the single post page
        response = client.get(f"/posts/{post.id}/")

        # Assert: Full content is visible
        assert response.status_code == 200
        assert "Understanding CSP" in response.content.decode()
        assert "Content Security Policy is crucial" in response.content.decode()

    def test_draft_post_returns_404(self, client):
        """Given a draft post, visiting its URL returns 404."""
        # Arrange: Create a draft post
        post = Post.objects.create(
            title="Draft Ideas",
            content="This is not ready...",
        )

        # Act: Try to visit the draft post
        response = client.get(f"/posts/{post.id}/")

        # Assert: Not found
        assert response.status_code == 404
