from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Meal
from .serializers import MealSerializer

def meal_list(request):
    return JsonResponse({
        "meals": []  # You'll populate this with actual data later
    }) 

class MealViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows meals to be viewed or edited.
    """
    queryset = Meal.objects.all().order_by('-created_at')
    serializer_class = MealSerializer
    permission_classes = [AllowAny] 