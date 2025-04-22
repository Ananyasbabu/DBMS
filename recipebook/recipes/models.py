from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    """Custom user model with profile picture support."""
    profile_picture = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

class Ingredient(models.Model):
    """Model representing individual ingredients."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    """Model for recipes, linking to multiple ingredients."""
    title = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient)
    instructions = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class UserWeight(models.Model):
    """Model for tracking user weight and BMI progress."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="weight_records")
    date = models.DateField(auto_now_add=True)
    weight = models.FloatField()
    bmi = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - Weight: {self.weight} kg, BMI: {self.bmi} ({self.date})"
