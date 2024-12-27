from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("view_listing/<int:listing_id>", views.view_listing, name="view_listing"),
    path("update_bid", views.update_bid, name="update_bid"),
    path("close_listing", views.close_listing, name="close_listing"),
    path("add_comment", views.add_comment, name="add_comment"),
    path('category', views.category, name="category"),
    path('watch_list', views.watch_list, name="watch_list"),
    path('add_watch_list', views.add_watch_list, name="add_watch_list"),
    path('remove_watch_list', views.remove_watch_list, name="remove_watch_list"),

]
