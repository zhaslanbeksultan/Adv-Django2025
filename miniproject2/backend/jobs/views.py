# resumes/views.py
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from jobs.models import JobListing
from jobs.serializers import JobListingSerializer
from resumes.models import Resume
import os
import logging
logger = logging.getLogger(__name__)

# Load skills from skills.txt (same as tasks.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_FILE = os.path.join(BASE_DIR, 'resumes', 'skills.txt')

with open(SKILLS_FILE, 'r') as f:
    SKILLS = {line.strip().lower() for line in f if line.strip()}

class JobRecommendationsView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Ensure the user is a job seeker
        # if request.user.role != 'job_seeker':
        #     return Response({"error": "Only job seekers can access job recommendations"},
        #                    status=status.HTTP_403_FORBIDDEN)

        # Get the latest processed resume for the user
        # resume = Resume.objects.filter(user=request.user, processed=True).last()
        resume = Resume.objects.last()
        if not resume:
            return Response({"error": "No processed resume found. Please upload and process a resume first."},
                           status=status.HTTP_404_NOT_FOUND)

        # Extract skills from the resume
        extracted_data = resume.extracted_data or {}
        resume_skills = set(skill.lower() for skill in extracted_data.get('skills', []))

        if not resume_skills:
            return Response({"error": "No skills found in your resume to match jobs."},
                           status=status.HTTP_400_BAD_REQUEST)

        # Get all active job listings
        job_listings = JobListing.objects.filter(is_active=True)

        # Match jobs based on skills
        recommended_jobs = []
        for job in job_listings:
            # Extract skills from job description using the same SKILLS set
            job_description = job.description.lower()
            words = set(job_description.split())
            job_skills = [skill for skill in SKILLS if skill in words]

            if not job_skills:  # Skip jobs with no detectable skills
                continue

            # Calculate skill overlap
            job_skills_set = set(job_skills)
            common_skills = resume_skills.intersection(job_skills_set)
            match_score = len(common_skills) / len(job_skills_set) * 100 if job_skills_set else 0  # Percentage match

            if match_score > 20:  # Threshold for relevance (adjustable)
                recommended_jobs.append({
                    'job_id': job.id,
                    'title': job.title,
                    'company': job.company,
                    'location': job.location,
                    'description': job.description,
                    'posted_by': job.posted_by.username,
                    'created_at': job.created_at.isoformat(),
                    'match_score': round(match_score, 2),
                    'matched_skills': list(common_skills)
                })

        # Sort by match score (highest first)
        recommended_jobs.sort(key=lambda x: x['match_score'], reverse=True)

        return Response({
            "message": "Recommended jobs based on your resume skills",
            "recommendations": recommended_jobs
        }, status=status.HTTP_200_OK)


@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache for 15 min
class JobListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        logger.info("View logic executed — this should appear only once if cache works.")
        jobs = JobListing.objects.filter(is_active=True)
        serializer = JobListingSerializer(jobs, many=True)
        return Response({"jobs": serializer.data}, status=status.HTTP_200_OK)

class JobCreateView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = JobListingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            job = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobUpdateView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def put(self, request, job_id):
        if request.user.role != 'recruiter':
            return Response({"error": "Only recruiters can update jobs"}, status=status.HTTP_403_FORBIDDEN)

        try:
            job = JobListing.objects.get(id=job_id, posted_by=request.user)
        except JobListing.DoesNotExist:
            return Response({"error": "Job not found or not owned by you"}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobListingSerializer(job, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobDeleteView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, job_id):
        # if request.user.role != 'recruiter':
        #     return Response({"error": "Only recruiters can delete jobs"}, status=status.HTTP_403_FORBIDDEN)

        try:
            job = JobListing.objects.get(id=job_id, posted_by=request.user)
        except JobListing.DoesNotExist:
            return Response({"error": "Job not found or not owned by you"}, status=status.HTTP_404_NOT_FOUND)

        job.delete()
        return Response({"message": "Job deleted successfully"}, status=status.HTTP_204_NO_CONTENT)