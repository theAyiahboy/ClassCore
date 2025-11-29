from django.contrib.auth.models import AbstractUser
from django.db import models

# 1. The Custom User Model
# We extend AbstractUser to keep Django's login/password magic,
# but we add our own "Role" field.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.ADMIN)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)


# 2. The Class Model (The Classroom)
class Class(models.Model):
    name = models.CharField(max_length=50)  # e.g., "JHS 2 - A"
    academic_year = models.CharField(max_length=20, default="2024/2025")
    
    # RELATIONSHIP: One Teacher manages One Class.
    # null=True: A class might exist without a teacher assigned yet.
    # on_delete=SET_NULL: If we fire the teacher, the class shouldn't vanish.
    class_master = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='class_managed'
    )

    def __str__(self):
        return self.name


# 3. The Student Model
class Student(models.Model):
    # RELATIONSHIP: One User Account = One Student Profile.
    # on_delete=CASCADE: If we delete the User login, delete the Student profile too.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    admission_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    
    # RELATIONSHIP: Many Students belong to One Class.
    current_class = models.ForeignKey(
        Class, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.admission_number})"
    

# 4. The Teacher Model
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} (Staff ID: {self.staff_id})"

# 5. The Subject Model
class Subject(models.Model):
    name = models.CharField(max_length=100) # e.g., "Integrated Science"
    is_core = models.BooleanField(default=True) # Checked = Core, Unchecked = Elective

    def __str__(self):
        return self.name

# 6. The Schedule (Who teaches What to Whom)
# This is a "Pivot Table" connecting Class, Subject, and Teacher
class ClassSubject(models.Model):
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    class Meta:
        # Prevent assigning the same subject twice to the same class
        unique_together = ['class_assigned', 'subject']

    def __str__(self):
        return f"{self.subject.name} for {self.class_assigned.name}"