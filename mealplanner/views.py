from django.http import JsonResponse

def index(request):
    return JsonResponse({
        "status": "success",
        "message": "Welcome to Meal Planner API",
        "endpoints": {
            "meals": "/api/meals/",
            # Add more endpoints as you create them
        },
        "documentation": "https://github.com/chandang206/meal-planner",  # Update with your docs URL
        "version": "1.0.0"
    }) 