from django.contrib import admin
from django.urls import path
from meals import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('meal/<int:pk>/', views.meal_detail, name='meal_detail'),
]