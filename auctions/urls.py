from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("viewitem/<int:itemid>", views.viewitem, name="viewitem"),
    path("createlisting", views.newitem, name="newitem"),
    path("category/<int:categoryid>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("placebid/<int:itemid>", views.viewitem, name="placebid"),
    path("writecomment/<int:itemid>", views.viewitem, name="writecomment"),
    path("addwatchlist/<int:itemid>", views.addwatchlist, name="addwatchlist"),
    path("deletecomment/<int:commentid>", views.deletecomment, name="deletecomment"),
    path("closedlists", views.closedlists, name="closedlists"),
    path("closedlist/<int:itemid>", views.closedlist, name="closedlist")
    
]
