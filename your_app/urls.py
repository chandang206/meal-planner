from django.urls import path
from . import views

urlpatterns = [
    # Your app's URL patterns
    path('your-endpoint/', views.your_view, name='your-view'),
] 