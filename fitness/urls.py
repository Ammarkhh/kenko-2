from django.urls import path

from fitness.views import WorkoutView, ProgramView

urlpatterns = [
    path("workout", WorkoutView.as_view()),
    path("program", ProgramView.as_view()),
]
