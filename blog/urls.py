from django.urls import path
from blog.views import homepage, single_post

urlpatterns = [
    path("", homepage, name="homepage"),
    path("posts/<int:post_id>/", single_post, name="single_post"),
]
