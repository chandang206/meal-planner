from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.db import IntegrityError
from django.urls import reverse 
from django.contrib import messages
from .models import Recipe, Ingredients, MealPlan
from .forms import RecipeForm, IngredientFormSet
from datetime import datetime, timedelta
import calendar



# Create your views here.
@login_required
def index(request):
    # Get all recipes for the logged-in user
    recipes = Recipe.objects.filter(author=request.user).order_by('-date')
    
    # Calendar data
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    
    # Get the current week
    calendar_week = []
    today = current_date.date()
    monday = today - timedelta(days=today.weekday())  # Get Monday of current week
    
    for i in range(7):
        day_date = monday + timedelta(days=i)
        calendar_week.append({
            'date': day_date,
            'day': day_date.day,
            'weekday': day_date.strftime('%a')  # Mon, Tue, etc.
        })
    
    # Get all planned meals for this week
    week_start = monday
    week_end = monday + timedelta(days=6)
    planned_meals = MealPlan.objects.filter(
        user=request.user,
        time__range=[week_start, week_end]
    ).select_related('recipe')
    
    # Create a dictionary of meals by date
    meal_dict = {}
    for meal in planned_meals:
        date_key = meal.time.day
        if date_key not in meal_dict:
            meal_dict[date_key] = []
        meal_dict[date_key].append(meal)

    return render(request, "recipes/index.html", {
        "recipes": recipes,
        "calendar_week": calendar_week,
        "month": current_date.strftime('%B'),  # Full month name
        "year": year,
        "meal_dict": meal_dict
    })

def login_view(request):
    # Try to log in user
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        # Check if user is authenticated
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "recipes/login.html",{
                "message": "Invalid username or/and password"
            })
    return render(request, "recipes/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # password and confirmation must match    
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "recipes/register",{
                "message": "Passwords must match"
            })
        
        # Create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "recipes/register.html",{
                "message":"Username already taken"
            })
        login(request,user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "recipes/register.html")

@login_required
def add_recipe(request):
    if request.method == "POST":
        recipe_form = RecipeForm(request.POST)
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            ingredient_formset = IngredientFormSet(request.POST, instance=recipe)
            if ingredient_formset.is_valid():
                ingredient_formset.save()
                messages.success(request, "Recipe added successfully!", extra_tags='persistent')
                return HttpResponseRedirect(reverse('recipe_detail', args=[recipe.id]))
            else:
                messages.error(request, "Please check the ingredient forms for errors.")
        else:
            messages.error(request, "Please correct the errors in the recipe form.")
    else:
        recipe_form = RecipeForm()
        ingredient_formset = IngredientFormSet()
    
    return render(request, "recipes/add_recipe.html", {
        "recipe_form": recipe_form,
        "ingredient_formset": ingredient_formset,
    })

@login_required
def plan_meal(request):
    if request.method == "POST":
        date = request.POST.get('date')
        recipe_id = request.POST.get('recipe')
        meal_type = request.POST.get('meal_type')
        servings = request.POST.get('servings')
        notes = request.POST.get('notes')

        try:
            recipe = Recipe.objects.get(id=recipe_id, author=request.user)
            
            existing_meal = MealPlan.objects.filter(
                user=request.user,
                time=date,
                meal_type=meal_type
            ).first()
            
            if existing_meal:
                messages.error(request, f"You already have a {meal_type} planned for this date.")
            else:
                meal_plan = MealPlan.objects.create(
                    user=request.user,
                    time=date,
                    recipe=recipe,
                    meal_type=meal_type,
                    servings=servings,
                    notes=notes
                )
                messages.success(request, f"Successfully planned {recipe.title} for {meal_type}!", extra_tags='persistent')
            
        except Recipe.DoesNotExist:
            messages.error(request, "Recipe not found.")
        except Exception as e:
            messages.error(request, f"Error planning meal: {str(e)}")
        
        return HttpResponseRedirect(reverse('index'))

    # If GET request, redirect to index
    return HttpResponseRedirect(reverse('index'))

@login_required
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=request.user)
    ingredients = recipe.ingredients.all()
    return render(request, "recipes/recipe_detail.html", {
        "recipe": recipe,
        "ingredients": ingredients,
    })

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=request.user)
    
    if request.method == "POST":
        recipe_form = RecipeForm(request.POST, instance=recipe)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe)
        
        if recipe_form.is_valid() and ingredient_formset.is_valid():
            recipe = recipe_form.save()
            ingredient_formset.save()
            messages.success(request, "Recipe updated successfully!", extra_tags='persistent')
            return HttpResponseRedirect(reverse('recipe_detail', args=[recipe.id]))
        else:
            if not recipe_form.is_valid():
                messages.error(request, f"Recipe form errors: {recipe_form.errors}")
            if not ingredient_formset.is_valid():
                messages.error(request, f"Ingredient form errors: {ingredient_formset.errors}")
    else:
        recipe_form = RecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe)
    
    return render(request, "recipes/edit_recipe.html", {
        "recipe_form": recipe_form,
        "ingredient_formset": ingredient_formset,
        "recipe": recipe
    })

@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=request.user)
    
    if request.method == "POST":
        recipe.delete()
        messages.success(request, "Recipe deleted successfully!", extra_tags='persistent')
        return HttpResponseRedirect(reverse('index'))
        
    return render(request, "recipes/delete_recipe.html", {
        "recipe": recipe
    })

