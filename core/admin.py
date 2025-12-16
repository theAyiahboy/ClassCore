from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Class, Teacher, Subject, ClassSubject, Attendance, Grade

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

# 3. Student Admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'admission_number', 'current_class')
    search_fields = ('admission_number', 'user__username')

# 4. Teacher Admin
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'staff_id')

# 5. Subject Admin
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_core')

# 6. Schedule Admin
@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ('class_assigned', 'subject', 'teacher')


# 7. Attendance Admin
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_assigned', 'date', 'status')
    list_filter = ('date', 'class_assigned', 'status')

# 8. Grade Admin
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'assessment_type', 'score', 'term')
    
    
    list_filter = ('subject', 'student__current_class', 'term')