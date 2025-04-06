from django.db import models

from user_auth.models import User


class Resume(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='resumes',
        limit_choices_to={'role': 'job_seeker'}  # Restrict to job seekers in admin/forms
    )
    file = models.FileField(upload_to='resumes/uploads')
    title = models.CharField(max_length=100, blank=True)
    extracted_data = models.JSONField(null=True, blank=True)  # Skills, experience, etc.
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.title or self.file.name}"
