from .models import Ingredient
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserWeight
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.shortcuts import redirect






def home(request):
    return render(request, "recipes/index.html")


def bmi_calculator(request):
    return render(request, "recipes/bmi.html")

def ingredient_book(request):
    return render(request, "recipes/ingredients.html")

def leaderboard(request):
    return render(request, "recipes/leaderboard.html")


@csrf_exempt
def add_ingredient(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Ingredient.objects.get_or_create(name=name.strip().lower())
        return JsonResponse({"message": "Ingredient added successfully!"})
    return JsonResponse({"error": "Invalid request method"}, status=400)


def get_ingredients(request):
    ingredients = list(Ingredient.objects.values_list("name", flat=True))
    return JsonResponse({"ingredients": ingredients})

@csrf_exempt
def delete_ingredient(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Ingredient.objects.filter(name=name.strip().lower()).delete()
            return JsonResponse({"message": "Ingredient deleted successfully!"})
    return JsonResponse({"error": "Invalid request method"}, status=400)


def leaderboard(request):
    return render(request, "recipes/leaderboard.html")


def get_weight_data(request):
    weight_entries = UserWeight.objects.order_by("date")[:5]  # Latest 5 entries
    data = {
        "labels": [entry.date.strftime("%d-%m-%Y") for entry in weight_entries],
        "values": [entry.weight for entry in weight_entries],
    }
    return JsonResponse(data)

def submit_bmi(request):
    if request.method == "POST":
        weight = float(request.POST.get("weight"))
        height = float(request.POST.get("height")) / 100
        bmi = weight / (height ** 2)
        
        UserWeight.objects.create(weight=weight, bmi=bmi)
        
        return JsonResponse({"message": "BMI recorded successfully!", "bmi": round(bmi, 2)})
    return JsonResponse({"error": "Invalid request"}, status=400)


def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect("profile")
        else:
            return render(request, "recipes/login.html", {"error": "Invalid credentials"})

    return render(request, "recipes/login.html")

def user_profile(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "recipes/profile.html", {"user": request.user})



@login_required
def edit_profile(request):
    if request.method == "POST" and "profile_picture" in request.FILES:
        user = request.user
        user.profile_picture = request.FILES["profile_picture"]
        user.save()
        return redirect("profile")

    return render(request, "recipes/edit_profile.html")