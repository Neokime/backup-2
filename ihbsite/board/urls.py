from django.urls import path
from . import views

app_name = "board"

urlpatterns = [
    path("create/", views.create_board, name="create"),
    path("list/", views.get_boards, name="list"),
    path("<int:board_id>/", views.get_board, name="read"),
    path("<int:board_id>/update/", views.update_board, name="update"),
    path("<int:board_id>/delete/", views.delete_board, name="delete"),
    path("", views.get_boards, name="list")
]
