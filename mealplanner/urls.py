from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="Meal Planner API",
      default_version='v1',
      description="""
      Welcome to the Meal Planner API documentation.
      
      This API allows you to:
      - Create, read, update and delete meals
      - View meal details including ingredients and instructions
      - Manage cooking times and servings
      
      Try out the endpoints using the interactive interface below.
      """,
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="your.email@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/', include('meals.urls')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]