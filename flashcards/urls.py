from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("viewcard/<int:cardid>", views.viewcard, name="viewcard"),
    path("createcard", views.newcard, name="newcard"),
    path("category/<int:categoryid>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("writecomment/<int:cardid>", views.viewcard, name="writecomment"),
    path("addwatchlist/<int:cardid>", views.addwatchlist, name="addwatchlist"),
    path("deletecomment/<int:commentid>", views.deletecomment, name="deletecomment")    
]
