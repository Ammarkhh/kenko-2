from django.urls import path

from forefront import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("fitness", views.fitness_view, name="fitness"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("hub", views.hub_view, name="hub"),
]
