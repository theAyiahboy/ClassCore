from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    #  defining roles as a standard TextChoice structure
    # This acts like an Enum (Enumeration) in other languages
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"

    # add a 'role' field to the standard Django user
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.ADMIN)

    # This method ensures that if a user is created as a 'superuser' ,
    # they are automatically marked as an Admin in our system too.
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)