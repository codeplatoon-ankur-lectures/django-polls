
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.question_list, name="question-list"),
    path("question/<int:question_id>", views.question_detail, name="question-detail"),
    path("question/<int:question_id>/edit", views.question_edit, name="question-edit")
]