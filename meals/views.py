from django.http import JsonResponse

def meal_list(request):
    return JsonResponse({
        "meals": []  # You'll populate this with actual data later
    }) 