import pytest
from django.utils import timezone
from blog.models import Post


@pytest.mark.django_db
class TestMarkdownRendering:
    """Blog post content written in Markdown renders to formatted HTML."""

    def test_common_markdown_renders_to_html(self, client):
        """Common Markdown syntax renders to formatted HTML."""
        # Arrange: Create a post with various Markdown syntax
        post = Post.objects.create(
            title="Markdown Test",
            content="""# Heading 1
A paragraph with **bold** and *italic* text.

## Heading 2
- List item 1
- List item 2

[A link](https://example.com)""",
            published_at=timezone.now(),
        )

        # Act: View the post
        response = client.get(f"/posts/{post.id}/")

        # Assert: Markdown is rendered to HTML
        assert response.status_code == 200
        content = response.content.decode()

        # Headings become <h1>, <h2>
        assert "<h1>" in content
        assert "Heading 1" in content
        assert "<h2>" in content
        assert "Heading 2" in content

        # Bold and italic
        assert "<strong>" in content or "<b>" in content
        assert "bold" in content
        assert "<em>" in content or "<i>" in content
        assert "italic" in content

        # Lists
        assert "<li>" in content
        assert "List item 1" in content
        assert "List item 2" in content

        # Links
        assert '<a href="https://example.com"' in content
        assert "A link" in content

    def test_code_blocks_have_syntax_highlighting(self, client):
        """Fenced code blocks are syntax-highlighted."""
        # Arrange: Create a post with a code block
        post = Post.objects.create(
            title="Code Test",
            content="""```python
def hello():
    print("Hello, World!")
```""",
            published_at=timezone.now(),
        )

        # Act: View the post
        response = client.get(f"/posts/{post.id}/")

        # Assert: Code is highlighted with Pygments classes
        assert response.status_code == 200
        content = response.content.decode()

        # Code block is rendered
        assert "<pre" in content or "<code" in content
        # Pygments adds CSS classes for syntax highlighting
        assert "class=" in content  # syntax highlighting uses classes
        # Function name should be in the output
        assert "hello" in content or "def" in content

    def test_markdown_is_safe_no_xss(self, client):
        """Markdown rendering is safe — no script execution possible."""
        # Arrange: Create a post with malicious script tags
        post = Post.objects.create(
            title="XSS Test",
            content='<script>alert("XSS")</script> Regular text.',
            published_at=timezone.now(),
        )

        # Act: View the post
        response = client.get(f"/posts/{post.id}/")

        # Assert: Script is NOT executed (escaped or removed)
        assert response.status_code == 200
        content = response.content.decode()

        # Script tags should be escaped or removed
        assert "<script>" not in content or "&lt;script&gt;" in content
        # The content should still be visible as text
        assert "Regular text" in content
