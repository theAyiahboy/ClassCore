from rest_framework import serializers
from .models import User, Class, Student, Teacher, Subject, ClassSubject

# 1. User Serializer (Translates the User Model)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role'] # We NEVER share the password

# 2. Class Serializer (Translates the Class Model)
class ClassSerializer(serializers.ModelSerializer):
    # Field 1: For DISPLAY (Shows full details) - Read Only
    class_master_details = UserSerializer(source='class_master', read_only=True)
    
    # Field 2: For WRITING (Select by ID) - Write Only
    class_master = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='TEACHER'), # Only allow Teachers!
        required=False, 
        allow_null=True
    )

    class Meta:
        model = Class
        # Note: We list both fields here
        fields = ['id', 'name', 'academic_year', 'class_master', 'class_master_details']
# 3. Student Serializer (Translates the Student Model)
class StudentSerializer(serializers.ModelSerializer):
    # READ-ONLY Fields (For Displaying Data)
    # These show the full details (Name, Email, Class Name) when you view the list
    user_details = UserSerializer(source='user', read_only=True)
    class_details = ClassSerializer(source='current_class', read_only=True)

    # WRITE Fields (For the Form)
    # These allow you to select the ID from a dropdown when creating a student
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        write_only=True
    )
    current_class = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Student
        # We list ALL fields here so the API handles them correctly
        fields = [
            'id', 
            'user',          # Input (Dropdown)
            'user_details',  # Output (Full Info)
            'admission_number', 
            'date_of_birth', 
            'current_class', # Input (Dropdown)
            'class_details', # Output (Full Info)
            'enrolled_at'
        ]
# 4. Teacher Serializer
class TeacherSerializer(serializers.ModelSerializer):
    # READ-ONLY: Shows full details (e.g., "Mr. Osei") in the list
    user_details = UserSerializer(source='user', read_only=True)

    # WRITE-ONLY: Shows a dropdown to pick the user ID
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='TEACHER'), # Only list Teachers!
        write_only=True
    )

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'user_details', 'staff_id', 'phone_number']

# 5. Subject Serializer
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'is_core']