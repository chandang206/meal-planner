from django.urls import path
from . import views

urlpatterns = [
    path('meals/', views.meal_list, name='meal-list'),
    # Add other meal-related endpoints here
] 