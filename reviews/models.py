from django.db import models
from django.core.exceptions import ValidationError
from users.models import User
from apartments.models import Apartment


# Create your models here.
class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')

    # Review Target: Can be a Person OR an Apartment
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews', null=True,
                                      blank=True)
    reviewed_apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='reviews', null=True,
                                           blank=True)

    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Ensure exactly one target is selected
        if not self.reviewed_user and not self.reviewed_apartment:
            raise ValidationError("A review must target either a user or an apartment.")
        if self.reviewed_user and self.reviewed_apartment:
            raise ValidationError("A review cannot target both a user and an apartment simultaneously.")

        # Prevent self-reviewing
        if self.reviewed_user == self.reviewer:
            raise ValidationError("You cannot review yourself.")

    def __str__(self):
        target = self.reviewed_user.username if self.reviewed_user else self.reviewed_apartment.name
        return f"[{self.rating}★] {self.reviewer.username} reviewed {target}"