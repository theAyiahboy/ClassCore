from django.contrib.auth.models import AbstractUser
from django.db import models

# ==========================================
# 1. CUSTOM USER MODEL
# ==========================================
class User(AbstractUser):
    """
    Extends the standard Django User model to include a 'role' field.
    This allows us to distinguish between Admins, Teachers, and Students
    using a single authentication system.
    """
    
    # Defining an Enumeration for roles ensures strict data consistency.
    # Users cannot be created with a role like "Principal" or "Janitor" unless defined here.
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"

    # The role field acts as the primary filter for permissions later on.
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.ADMIN)

    def save(self, *args, **kwargs):
        """
        Overriding the save method to handle automatic role assignment.
        If a user is created as a 'superuser' via command line, 
        we automatically set their role to ADMIN to prevent logic errors.
        """
        if self.is_superuser:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)


# ==========================================
# 2. ACADEMIC MODELS
# ==========================================

class Class(models.Model):
    """
    Represents a physical class or grade level (e.g., 'JHS 2 - A').
    """
    name = models.CharField(max_length=50)  # Example: "Basic 4"
    academic_year = models.CharField(max_length=20, default="2024/2025")
    
    # RELATIONSHIP: ForeignKey (Many-to-One)
    # Logic: One Class is managed by One Teacher (The Class Master).
    # on_delete=SET_NULL: If the teacher leaves, the class should remain (just without a master).
    class_master = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='class_managed' 
        # 'related_name' allows us to find the class via user.class_managed
    )

    def __str__(self):
        return self.name


class Student(models.Model):
    """
    Stores academic profiles. Linked 1-to-1 with a User account.
    Separating 'User' and 'Student' keeps authentication logic clean.
    """
    # RELATIONSHIP: One-to-One
    # Logic: Deleting the User account (Login) automatically deletes the Student profile.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    admission_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    
    # RELATIONSHIP: ForeignKey
    # Logic: A student belongs to ONE class, but a class has MANY students.
    current_class = models.ForeignKey(
        Class, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    enrolled_at = models.DateTimeField(auto_now_add=True) # Auto-timestamps when created

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.admission_number})"


class Teacher(models.Model):
    """
    Stores staff profiles. Linked 1-to-1 with a User account.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} (Staff ID: {self.staff_id})"


class Subject(models.Model):
    """
    Represents a subject in the curriculum (e.g., 'Integrated Science').
    Does not link to a teacher directly, because multiple teachers might teach 'Science'.
    """
    name = models.CharField(max_length=100) 
    is_core = models.BooleanField(default=True) # Boolean to distinguish Core vs Elective

    def __str__(self):
        return self.name


class ClassSubject(models.Model):
    """
    The 'Schedule' Model (Pivot Table).
    This answers the question: "Who teaches Subject X to Class Y?"
    """
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    # Logic: We can assign a specific teacher to this specific subject-class combo.
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    class Meta:
        # CONSTRAINT: Prevents duplicate entries. 
        # A class cannot have 'Mathematics' assigned twice.
        unique_together = ['class_assigned', 'subject']
        verbose_name = "Class Schedule"
        verbose_name_plural = "Class Schedules"

    def __str__(self):
        return f"{self.subject.name} for {self.class_assigned.name}"



# Attendance Model
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(
        max_length=10, 
        choices=[('PRESENT', 'Present'), ('ABSENT', 'Absent')], 
        default='PRESENT'
    )

    class Meta:
        # CONSTRAINT: A student can only be marked once per day
        unique_together = ['student', 'date']

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"

#  Grade Model (Assessment)
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assessment_type = models.CharField(
        max_length=20,
        choices=[('TEST', 'Class Test'), ('EXAM', 'Exam'), ('PROJECT', 'Project')],
        default='TEST'
    )
    score = models.DecimalField(max_digits=5, decimal_places=2) # e.g. 85.50
    term = models.CharField(max_length=20, default="First Term")
    date_recorded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.score}"