import random
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ]

COURSE_CHOICES = [
    ('csai', 'BTech CSAI'),
    ('csds', 'BTech CSDS'),
    ('dsai', 'BTech DS & Analytics'),
    ('design', 'Design'),
    ('psych', 'Psychology'),
    ('bba', 'BBA'),
    ]

class UserProfile(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    sleep_schedule = models.CharField(max_length=50)  # e.g., Night Owl, Early Bird
    cleanliness = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    introvert_extrovert = models.CharField(max_length=50)  # e.g., Introvert
    interests = models.TextField()  # Comma-separated or plain text
    is_submitted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    course = models.CharField(max_length=20, choices=COURSE_CHOICES, null=True)
    

    def __str__(self):
        return self.full_name

class MatchResult(models.Model):
    student1 = models.ForeignKey('UserProfile', related_name='match_initiator', on_delete=models.CASCADE)
    student2 = models.ForeignKey('UserProfile', related_name='match_partner', on_delete=models.CASCADE)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student1.full_name} 🤝 {self.student2.full_name} (Score: {self.score})"
    

class EmailOTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() - self.created_at < timezone.timedelta(minutes=5)   


class StudentUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Email is required")
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

class StudentUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    has_submitted_form = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = StudentUserManager()

    def __str__(self):
        return self.email