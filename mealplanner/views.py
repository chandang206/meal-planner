from django.http import JsonResponse

def index(request):
    return JsonResponse({
        "status": "success",
        "message": "Welcome to Meal Planner API"
    }) 