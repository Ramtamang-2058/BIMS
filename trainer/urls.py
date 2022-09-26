from django.urls import path
from trainer import views

urlpatterns = [
    path('', views.trainer_dashboard, name="trainer_dashboard"),
    path('update/', views.profile_update, name="profileUpdate"),
    path('dashbiard/', views.sidebar),
]
