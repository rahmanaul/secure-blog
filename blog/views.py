from django.shortcuts import render
from django.http import Http404
from blog.models import Post


def homepage(request):
    """Display a list of published blog posts."""
    posts = Post.objects.filter(published_at__isnull=False)
    return render(request, "blog/homepage.html", {"posts": posts})


def single_post(request, post_id):
    """Display a single published blog post."""
    try:
        post = Post.objects.get(id=post_id, published_at__isnull=False)
    except Post.DoesNotExist:
        raise Http404("Post not found")
    return render(request, "blog/single_post.html", {"post": post})
