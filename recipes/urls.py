from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("add_recipe/", views.add_recipe, name="add_recipe"),
    path("plan_meal", views.plan_meal, name="plan_meal"),
    path("recipe/<int:recipe_id>/", views.recipe_detail, name="recipe_detail"),
    path("recipe/<int:recipe_id>/edit/", views.edit_recipe, name="edit_recipe"),
    path("recipe/<int:recipe_id>/delete/", views.delete_recipe, name="delete_recipe"),

]