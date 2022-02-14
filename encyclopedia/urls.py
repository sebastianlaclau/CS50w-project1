from django.urls import path

from . import views

urlpatterns = [
    path("wiki/create", views.create, name="create_url"),
    path("wiki/random", views.redirect, name="redirect_url"),
    path("wiki/<str:filename>/edit", views.edit, name="edit_url"),
    path("wiki/<str:filename>", views.get_entry, name="entry_url"),
    path("", views.index, name="index"),
]
