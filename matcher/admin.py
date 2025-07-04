from django.contrib import admin
from .models import UserProfile, MatchResult, StudentUser

admin.site.register(StudentUser)
admin.site.register(UserProfile)
admin.site.register(MatchResult) 