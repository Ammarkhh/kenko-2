from django.urls import path

from nutrition.views import MealView

urlpatterns = [
    path("meal", MealView.as_view()),
]
