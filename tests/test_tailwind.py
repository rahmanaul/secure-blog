import pytest
from django.utils import timezone
from blog.models import Post


@pytest.mark.django_db
class TestTailwindStyling:
    """Pages are styled with Tailwind CSS utility classes."""

    def test_homepage_has_tailwind_classes(self, client):
        """The homepage includes Tailwind CSS and utility classes."""
        # Arrange: Create a published post
        Post.objects.create(
            title="Security Post",
            content="Content here...",
            published_at=timezone.now(),
        )

        # Act: Visit homepage
        response = client.get("/")

        # Assert: Tailwind is loaded and classes are present
        assert response.status_code == 200
        content = response.content.decode()

        # Tailwind script or CDN should be present
        assert "tailwind" in content.lower()

        # Posts should have container classes for spacing
        assert "max-w" in content  # max-width utility

    def test_single_post_has_tailwind_classes(self, client):
        """The single post page includes Tailwind CSS and utility classes."""
        # Arrange: Create a published post
        post = Post.objects.create(
            title="Post Title",
            content="Post content...",
            published_at=timezone.now(),
        )

        # Act: Visit single post
        response = client.get(f"/posts/{post.id}/")

        # Assert: Tailwind is loaded and classes are present
        assert response.status_code == 200
        content = response.content.decode()

        # Tailwind script or CDN should be present
        assert "tailwind" in content.lower()

        # Typography utilities should be present
        assert "text-" in content  # text-size/color utilities
