from rest_framework import serializers
from .models import Meal

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'name', 'description', 'ingredients', 'instructions', 
                 'prep_time', 'cook_time', 'servings', 'created_at', 'updated_at'] 