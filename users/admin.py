from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PreferenceTag, LifestylePreference


# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'gender', 'verification_status', 'is_staff')
    list_filter = ('role', 'gender', 'verification_status', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ('Livo Custom Fields',
         {'fields': ('contact_link', 'profile_image', 'phone', 'gender', 'role', 'verification_status')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Livo Custom Fields', {
            'fields': ('first_name', 'last_name', 'email', 'contact_link', 'profile_image', 'phone', 'gender', 'role',
                       'verification_status')}),
    )


@admin.register(PreferenceTag)
class PreferenceTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(LifestylePreference)
class LifestylePreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'educational_institution', 'workplace')
    search_fields = ('user__email', 'educational_institution', 'workplace')
    filter_horizontal = ('preferences',)  # Better UI for ManyToMany field
