from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("viewcard/<int:cardid>", views.viewcard, name="viewcard"),
    path("createcard", views.newcard, name="newcard"),
    path("createcategory", views.newcategory, name="newcategory"),
    path("category/<int:categoryid>", views.category, name="category"),
    path("watchcard", views.watchcard, name="watchcard"),
    path("writecomment/<int:cardid>", views.viewcard, name="writecomment"),
    path("addwatchcard/<int:cardid>", views.addwatchcard, name="addwatchcard"),
    path("deletecomment/<int:commentid>", views.deletecomment, name="deletecomment")    
]
