from django.contrib import admin
from .models import Househelp, SkillTag

# Register your models here.

@admin.register(SkillTag)
class SkillTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Househelp)
class HousehelpAdmin(admin.ModelAdmin):
    list_display = ('user', 'expected_salary')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    filter_horizontal = ('skills',)
