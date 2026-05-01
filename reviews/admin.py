from django.contrib import admin
from reviews.models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('get_target', 'reviewer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('reviewer__username', 'reviewed_user__username', 'reviewed_apartment__name', 'comment')

    def get_target(self, obj):
        if obj.reviewed_user:
            return f"User: {obj.reviewed_user.username}"
        return f"Apartment: {obj.reviewed_apartment.name}"
    get_target.short_description = 'Target'