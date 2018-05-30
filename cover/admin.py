from django.contrib import admin
from .models import Board, SchoolProfile, StudentProfile
# Register your models here.
admin.site.register(Board)
admin.site.register(SchoolProfile)
admin.site.register(StudentProfile)
