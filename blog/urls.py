from django.urls import path
from blog.views import homepage, single_post, login, two_factor, admin_dashboard, logout

urlpatterns = [
    path("", homepage, name="homepage"),
    path("posts/<int:post_id>/", single_post, name="single_post"),
    path("login/", login, name="login"),
    path("2fa/", two_factor, name="2fa"),
    path("admin/", admin_dashboard, name="admin"),
    path("logout/", logout, name="logout"),
]
