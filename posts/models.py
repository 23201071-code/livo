from django.db import models
from django.core.exceptions import ValidationError
from users.models import User
from apartments.models import Apartment

from django.core.validators import MinValueValidator


# Create your models here.
class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('ROOM', 'Room Listing'),
        ('FOOD', 'Food Post'),
        ('HELP', 'Househelp Post'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                validators=[MinValueValidator(0)])

    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    apartment = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True, blank=True, related_name='listings')

    message_link = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField()
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        try:
            current_user = self.user
        except (User.DoesNotExist, AttributeError):
            return

        if self.type == 'ROOM' and current_user.role not in ['ROOMMATE', 'HOUSE_OWNER']:
            raise ValidationError(
                f"Only Roommates and House Owners can create Room Listings. Your role is {current_user.get_role_display()}.")

        if self.type == 'FOOD' and current_user.role != 'VENDOR':
            raise ValidationError(
                f"Only Vendors/Meal Providers can create Food Posts. Your role is {current_user.get_role_display()}.")

        if self.type == 'HELP' and current_user.role != 'HOUSE_HELP':
            raise ValidationError(
                f"Only House Help professionals can create Help Posts. Your role is {current_user.get_role_display()}.")

        if self.type == 'ROOM' and not self.apartment:
            raise ValidationError(
                "Room Listings MUST be linked to a physical Apartment entity. Please create/select an apartment first.")

        if self.type != 'ROOM' and self.apartment:
            raise ValidationError("Only Room Listings should be linked to an Apartment.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.get_type_display()}] {self.title}"