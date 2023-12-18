from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("feedback/<int:id>", views.feedback, name="feedback"),
    path("star_profile/<int:id>", views.star_profile, name="star_profile"),
    path("unstar_profile/<int:id>", views.unstar_profile, name="unstar_profile"),
    path("edit_profile/<int:id>", views.edit_profile, name="edit_profile"),
    path("search_tutors", views.search_tutors, name="search_tutors"),
    path("lesson_record", views.lesson_record, name="lesson_record"),
    path("add_lesson", views.add_lesson, name="add_lesson"),
    path("delete_lesson/<int:id>", views.delete_lesson, name="delete_lesson"),
    path("cancel_schedule/<int:id>", views.cancel_schedule, name="cancel_schedule"),
    path("add_availability", views.add_availability, name="add_availability"),
    path("delete_availability/<int:id>", views.delete_availability, name="delete_availability"),
    path("view_tutor_availability", views.view_tutor_availability, name="view_tutor_availability"),
    path("add_schedule/<int:id>", views.add_schedule, name="add_schedule"),
]
