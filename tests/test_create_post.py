import pytest
from django.contrib.auth.models import User
from blog.models import Post


@pytest.mark.django_db
class TestCreatePost:
    """Authenticated authors can create new blog posts."""

    def test_new_post_page_accessible_to_authenticated_users(self, client):
        """The new post form is accessible to logged-in users."""
        # Arrange: Create and login a user
        user = User.objects.create_user(username="author", password="testpass123")
        client.force_login(user)

        # Act: Visit new post page
        response = client.get("/admin/new-post/")

        # Assert: Form is displayed
        assert response.status_code == 200
        content = response.content.decode()
        assert 'name="title"' in content
        assert 'name="content"' in content
        assert "csrfmiddlewaretoken" in content

    def test_unauthenticated_user_cannot_access_new_post(self, client):
        """Unauthenticated users are redirected to login."""
        response = client.get("/admin/new-post/")
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_save_as_draft_creates_unpublished_post(self, client):
        """Saving as draft creates a post without published_at."""
        # Arrange: Create and login a user
        user = User.objects.create_user(username="author", password="testpass123")
        client.force_login(user)

        # Act: Submit form with save_as_draft
        response = client.post("/admin/new-post/", {
            "title": "My Draft Post",
            "content": "This is draft content",
            "save_as_draft": "Save as Draft",
        })

        # Assert: Post is created but not published
        assert response.status_code == 302
        post = Post.objects.get(title="My Draft Post")
        assert post.content == "This is draft content"
        assert post.published_at is None  # Draft

    def test_publish_creates_published_post(self, client):
        """Publishing creates a post with published_at set."""
        # Arrange: Create and login a user
        user = User.objects.create_user(username="author", password="testpass123")
        client.force_login(user)

        # Act: Submit form with publish
        response = client.post("/admin/new-post/", {
            "title": "My Published Post",
            "content": "This is published content",
            "publish": "Publish",
        })

        # Assert: Post is created and published
        assert response.status_code == 302
        post = Post.objects.get(title="My Published Post")
        assert post.content == "This is published content"
        assert post.published_at is not None  # Published
