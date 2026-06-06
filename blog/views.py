from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
import random
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


def login(request):
    """Login page for author authentication."""
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Valid credentials - generate 2FA code and redirect to 2FA page
            code = str(random.randint(100000, 999999))
            request.session["auth_user_id"] = user.id
            request.session["2fa_code"] = code
            # TODO: Send code via email
            return redirect("/2fa/")
        else:
            error = "Invalid username or password"

    return render(request, "blog/login.html", {"error": error})


def two_factor(request):
    """Two-factor authentication page."""
    error = None

    # Check if user has completed step 1
    user_id = request.session.get("auth_user_id")
    if not user_id:
        return redirect("/login/")

    if request.method == "POST":
        code = request.POST.get("code", "")
        expected_code = request.session.get("2fa_code")

        if code == expected_code:
            # Valid 2FA code - log the user in
            try:
                user = User.objects.get(id=user_id)
                auth_login(request, user)
                # Clear the temporary session data
                del request.session["auth_user_id"]
                del request.session["2fa_code"]
                return redirect("/admin/")
            except User.DoesNotExist:
                error = "User not found"
        else:
            error = "Invalid 2FA code"

    return render(request, "blog/2fa.html", {"error": error})


@login_required(login_url="/login/")
def admin_dashboard(request):
    """Admin dashboard for authenticated authors."""
    return render(request, "blog/admin.html")


def logout(request):
    """Logout the current user and terminate the session."""
    auth_logout(request)
    return redirect("/login/")


@login_required(login_url="/login/")
def new_post(request):
    """Create a new blog post."""
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        # Check if saving as draft or publishing
        if "save_as_draft" in request.POST:
            # Save as draft - no published_at
            post = Post.objects.create(title=title, content=content)
            return redirect("/admin/")
        elif "publish" in request.POST:
            # Publish - set published_at
            post = Post.objects.create(
                title=title,
                content=content,
                published_at=timezone.now()
            )
            return redirect("/admin/")

    return render(request, "blog/new_post.html")
