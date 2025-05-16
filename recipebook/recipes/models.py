from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model


def profile_pic_upload_path(instance, filename):
    """Generate upload path for profile pictures"""
    return f'profile_pics/user_{instance.id}/{filename}'

class CustomUser(AbstractUser):
    """Extended user model with profile picture and improved security"""
    email = models.EmailField(_('email address'), unique=True)  # ✅ Email must be unique
    profile_picture = models.ImageField(
        upload_to=profile_pic_upload_path,
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'  # ✅ Using email for authentication
    REQUIRED_FIELDS = ['username']

    # Permissions
    groups = models.ManyToManyField(Group, blank=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def save(self, *args, **kwargs):
        """Delete old profile picture when uploading a new one"""
        if self.pk:
            try:
                old_user = CustomUser.objects.get(pk=self.pk)
                if old_user.profile_picture and old_user.profile_picture != self.profile_picture:
                    old_user.profile_picture.delete(save=False)
            except CustomUser.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Delete profile picture when user is deleted"""
        if self.profile_picture:
            self.profile_picture.delete(save=False)
        super().delete(*args, **kwargs)

class Ingredient(models.Model):
    """Model representing user-specific ingredients"""
    user = models.ForeignKey(
        get_user_model(),  # ✅ Dynamically references CustomUser
        on_delete=models.CASCADE, 
        related_name="ingredients"
    )  
    name = models.CharField(
        max_length=100,
        help_text=_("Name of the ingredient")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "name"], name="unique_user_ingredient")
        ]
        ordering = ["name"]
        verbose_name = _("Ingredient")
        verbose_name_plural = _("Ingredients")

    def __str__(self):
        return f"{self.name} (User: {self.user.username})"



class UserWeight(models.Model):
    """Model for tracking user weight and BMI progress with validation"""
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name="weight_records"
    )  # ✅ Ensured user_id exists properly
    date = models.DateField(auto_now_add=True)
    weight = models.FloatField(
        validators=[
            MinValueValidator(20, message="Weight must be at least 20kg"),
            MaxValueValidator(300, message="Weight must be less than 300kg")
        ]
    )
    bmi = models.FloatField(
        validators=[
            MinValueValidator(10, message="Invalid BMI value"),
            MaxValueValidator(60, message="Invalid BMI value")
        ]
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = _('weight record')
        verbose_name_plural = _('weight records')
        get_latest_by = "date"

    def __str__(self):
        return f"{self.user.email}: {self.weight}kg on {self.date}"


class UserProfile(models.Model):
    """Additional user profile information"""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    height = models.FloatField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(100, message="Height must be at least 100cm"),
            MaxValueValidator(250, message="Height must be less than 250cm")
        ],
        help_text="Height in centimeters"
    )
    birth_date = models.DateField(null=True, blank=True)
    dietary_preferences = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Profile of {self.user.email}"
