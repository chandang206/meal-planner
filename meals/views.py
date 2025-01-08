from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from .models import Meal
from .serializers import MealSerializer

def meal_list(request):
    return JsonResponse({
        "meals": []  # You'll populate this with actual data later
    }) 

class MealViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing meals.
    """
    queryset = Meal.objects.all().order_by('-created_at')
    serializer_class = MealSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Get a list of all meals",
        operation_summary="List all meals"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new meal",
        operation_summary="Create meal"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Get details of a specific meal",
        operation_summary="Get meal details"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs) 