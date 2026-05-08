from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ('ROOMMATE', 'Roommate'),
        ('HOUSE_OWNER', 'House Owner'),
        ('HOUSE_HELP', 'House Help'),
    ]

    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact_link = models.URLField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    verification_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class PreferenceTag(models.Model):
    CATEGORY_CHOICES = [
        ('HABIT', 'Daily Habit'),
        ('SOCIAL', 'Social Life'),
        ('HOUSE', 'House Rule Preferences'),
        ('FOOD', 'Dietary/Food Style'),
    ]

    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='HABIT')

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class LifestylePreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lifestyle_preference')
    educational_institution = models.CharField(max_length=255, blank=True, null=True)
    workplace = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True, help_text="A short bio describing your lifestyle.")

    preferences = models.ManyToManyField(PreferenceTag, blank=True, related_name='users_with_preference')

    def __str__(self):
        return f"Lifestyle Profile: {self.user.email}"