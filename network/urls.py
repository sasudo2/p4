
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("get", views.get, name="get"),
    path("post", views.post, name="post"),
    path("load", views.load, name="load"),
    path("like", views.like, name="like"),
    path("profile/<str:user_name>", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("loadPost", views.loadPost, name="loadPost"),
    path("edit", views.edit, name="edit"),
]
