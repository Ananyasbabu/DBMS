from django.urls import path
from .views import home, bmi_calculator, ingredient_book, add_ingredient, get_ingredients, delete_ingredient
from .views import leaderboard, get_weight_data, submit_bmi
from .views import user_login, user_profile
from .views import edit_profile

urlpatterns = [
    path('', home, name='home'),
    path('bmi/', bmi_calculator, name='bmi'),
    path('ingredients/', ingredient_book, name='ingredients'),  # Fix: Changed to `ingredient_book`
    path("add_ingredient/", add_ingredient, name="add_ingredient"),
    path("get_ingredients/", get_ingredients, name="get_ingredients"),
     path("delete_ingredient/", delete_ingredient, name="delete_ingredient"),
     path("leaderboard/", leaderboard, name="leaderboard"),
    path("get_weight_data/", get_weight_data, name="get_weight_data"),
    path("submit_bmi/", submit_bmi, name="submit_bmi"),
    path("login/", user_login, name="login"),
    path("profile/", user_profile, name="profile"),
    path("edit_profile/", edit_profile, name="edit_profile"),
]

