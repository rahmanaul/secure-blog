from django.shortcuts import render
from django.http import Http404
from blog.models import Post
import markdown
import bleach


def homepage(request):
    """Display a list of published blog posts."""
    posts = Post.objects.filter(published_at__isnull=False)
    return render(request, "blog/homepage.html", {"posts": posts})


def single_post(request, post_id):
    """Display a single published blog post with markdown rendering."""
    try:
        post = Post.objects.get(id=post_id, published_at__isnull=False)
    except Post.DoesNotExist:
        raise Http404("Post not found")

    # Render markdown to HTML with syntax highlighting
    md = markdown.Markdown(extensions=['fenced_code', 'codehilite'])
    rendered_content = md.convert(post.content)

    # Sanitize HTML to prevent XSS - allow safe tags only
    # Allow markdown-generated tags but not scripts, iframes, etc.
    clean_content = bleach.clean(
        rendered_content,
        tags=['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
              'strong', 'em', 'b', 'i', 'u', 'a',
              'ul', 'ol', 'li', 'br', 'hr', 'blockquote',
              'pre', 'code', 'div', 'span'],
        attributes={'a': ['href'], '*': ['class']},
    )

    return render(request, "blog/single_post.html", {
        "post": post,
        "rendered_content": clean_content,
    })
