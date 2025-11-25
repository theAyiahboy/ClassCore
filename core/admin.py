from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # This controls what you see when you click on a user to edit them
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
    
    # This controls what you see when you add a NEW user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
    
    # This controls the columns in the list view (the table of all users)
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    
    # This adds filters on the right side (filter by Role!)
    list_filter = ('role', 'is_staff', 'is_active')

# Register your User model with this custom configuration
admin.site.register(User, CustomUserAdmin)