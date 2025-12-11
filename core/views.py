from rest_framework import viewsets
from .models import Class, Student, Teacher
from .serializers import ClassSerializer, StudentSerializer, TeacherSerializer
from .models import Class, Student, Teacher, Subject  # Added Subject
from .serializers import ClassSerializer, StudentSerializer, TeacherSerializer, SubjectSerializer # Added SubjectSerializer

# ... (Leave your other ViewSets alone)

# ==========================================
# THE LOGIC LAYER (Views)
# These classes decide what happens when a request comes in.
# ==========================================

class ClassViewSet(viewsets.ModelViewSet):
    """
    Handles: GET (List), POST (Create), PUT (Update), DELETE
    URL: /api/classes/
    """
    # 1. The Queryset: What data are we looking at? (All classes)
    queryset = Class.objects.all()
    # 2. The Serializer: How do we translate this data?
    serializer_class = ClassSerializer

class StudentViewSet(viewsets.ModelViewSet):
    """
    Handles: GET, POST, PUT, DELETE for Students
    URL: /api/students/
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    """
    Handles: GET, POST, PUT, DELETE for Teachers
    URL: /api/teachers/
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    """
    Handles: GET, POST, PUT, DELETE for Subjects
    URL: /api/subjects/
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer