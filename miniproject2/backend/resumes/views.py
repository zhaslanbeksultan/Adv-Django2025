from rest_framework import generics, permissions, status
from rest_framework.response import Response
from resumes.tasks import process_resume
from resumes.serializers import ResumeSerializer


class ResumeUploadView(generics.CreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        resume = serializer.save(user=self.request.user)
        process_resume.delay(resume.id)  # Run in background
        return Response({"message": "Resume uploaded successfully. Processing in progress."}, status=status.HTTP_201_CREATED)
