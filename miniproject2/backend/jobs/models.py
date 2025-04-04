from django.db import models

from user_auth.models import User


class Job(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'recruiter'})
    title = models.CharField(max_length=100)
    description = models.TextField()
    required_skills = models.JSONField(null=True, blank=True)  # e.g., {"skills": ["Java", "Spring"]}
    posted_at = models.DateTimeField(auto_now_add=True)
