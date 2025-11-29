from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Class, Teacher, Subject, ClassSubject

# 1. Custom User Admin
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')

admin.site.register(User, CustomUserAdmin)

# 2. Class Admin
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_master', 'academic_year')
    search_fields = ('name',)

# 3. Student Admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'admission_number', 'current_class', 'enrolled_at')
    search_fields = ('admission_number', 'user__username')
    list_filter = ('current_class',)

# --- NEW ADDITIONS ---

# 4. Teacher Admin
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'staff_id', 'phone_number')
    search_fields = ('user__username', 'staff_id')

# 5. Subject Admin
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_core')
    list_filter = ('is_core',)

# 6. ClassSubject Admin (The Schedule)
@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    # This shows: "JHS 1 | Math | Mr. Osei" in the list
    list_display = ('class_assigned', 'subject', 'teacher')
    # Filter by class so you can see "All subjects for JHS 1"
    list_filter = ('class_assigned', 'subject')