from django.urls import path

from resumes.views import ResumeUploadView, ResumeFeedbackView

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume_upload'),
    path('resume-feedback/', ResumeFeedbackView.as_view(), name='resume_feedback'),
]