from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, ClassViewSet, TeacherViewSet
from .views import StudentViewSet, ClassViewSet, TeacherViewSet, SubjectViewSet

# 1. The Router (The Automation Tool)
# Instead of writing every URL manually (like /students/create, /students/delete),
# The Router creates them ALL for us automatically.
router = DefaultRouter()

# 2. Registering the Routes
# We tell the router: "If someone asks for 'students', send them to StudentViewSet"
router.register(r'students', StudentViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'subjects', SubjectViewSet)

# 3. The URL Patterns
# This is the list that Django actually reads.
urlpatterns = [
    path('', include(router.urls)),
]

