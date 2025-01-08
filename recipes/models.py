from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(
        max_length=1000,
        blank=True,
        help_text="Enter an URL of your recipe image"
    )
    cook_time = models.PositiveIntegerField(help_text="Time in minutes")
    prep_time = models.PositiveIntegerField(help_text="Time in minutes")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"The {self.title} created by {self.author} at {self.date}" 

class Ingredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    units = [
        ('g','Grams'),
        ('kg','Kilograms'),
        ('ml','Millitmetters'),
        ('l','Liter'),
        ('cup','Cups'),
        ('tbsp','Tablespoons'),
        ('piece','Pieces'),
    ]
    unit = models.CharField(max_length=10, choices=units, default='g')

    def __str__(self):
        return f"{self.quantity} {self.get_unit_display()} of {self.name}"

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=20, choices=[
        ('breakfast',"Breakfast"),        
        ('lunch',"Lunch"),        
        ('dinner',"Dinner"),
        ('snack', "Snack")        
    ])

    servings = models.PositiveBigIntegerField(default=1)
    notes = models.TextField(blank=True)

    # Prevent duplicated meals
    class Meta:
        ordering = ['time', 'meal_type']
        unique_together = ['user', 'time', 'meal_type'] 