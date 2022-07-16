from django.urls import path

from trainer.views import SurveyView

urlpatterns = [
    path("survey", SurveyView.as_view()),
]
