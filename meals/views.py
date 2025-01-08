from django.shortcuts import render, get_object_or_404
from .models import Meal

def home(request):
    meals = Meal.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'meals': meals})

def meal_detail(request, pk):
    meal = get_object_or_404(Meal, pk=pk)
    return render(request, 'meals/meal_detail.html', {'meal': meal}) 