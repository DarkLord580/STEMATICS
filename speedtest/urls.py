from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("typing", views.typing, name="typing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("getstring", views.getstring, name="getstring"),
    path("score", views.score, name="score")    
]