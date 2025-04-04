from django.db import models

from user_auth.models import User


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'job_seeker'})
    file = models.FileField(upload_to='resumes/')
    title = models.CharField(max_length=100, blank=True)
    skills = models.JSONField(null=True, blank=True)  # e.g., {"skills": ["Python", "Django"]}
    feedback = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
