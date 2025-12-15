from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Import ALL your ViewSets in one place
from .views import (
    StudentViewSet, 
    ClassViewSet, 
    TeacherViewSet, 
    SubjectViewSet, 
    AttendanceViewSet, 
    GradeViewSet, 
    PaymentViewSet
)

# 1. Create the Router (The Map Maker)
router = DefaultRouter()

# 2. Register ALL endpoints here
router.register(r'students', StudentViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'payments', PaymentViewSet)

# 3. The URL Patterns
urlpatterns = [
    path('', include(router.urls)),
]