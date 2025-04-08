from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import permissions, status
from resumes.models import Resume
from resumes.serializers import ResumeSerializer
import requests
from resumes.tasks import process_resume
import json
from django.conf import settings
import re

class ResumeFeedbackView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get the latest processed resume
        resume = Resume.objects.filter(user=request.user, processed=True).last()
        if not resume:
            return Response({"error": "No processed resume found"}, status=status.HTTP_404_NOT_FOUND)

        extracted_data = resume.extracted_data
        text = extracted_data.get('text', '')
        skills = extracted_data.get('skills', [])
        sections = extracted_data.get('sections', {})

        # Prepare prompt for OpenRouter
        prompt = f"""
        Analyze this resume data for a Backend Developer role:
        - Text: {text}
        - Skills: {', '.join(skills)}
        - Sections: {json.dumps(sections)}

        Provide feedback in JSON format with these sections:
        1. "skill_gaps": 
           - "present": list of skills present
           - "missing": list of trending skills not present
           - "suggestion": natural language advice
        2. "formatting": 
           - List of suggestions or a string if no issues
        3. "ats_optimization": 
           - "present": list of ATS keywords present
           - "missing": list of ATS keywords not present
           - "suggestion": natural language advice

        Ensure the response is concise, actionable, and tailored to the data.
        """

        # Call OpenRouter API
        try:
            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {settings.OPENROUTER_API_KEY}',
                    'Content-Type': 'application/json',
                },
                json={
                    'model': 'meta-llama/llama-4-maverick:free',
                    'messages': [{'role': 'user', 'content': prompt}],
                    'response_format': {'type': 'json_object'}  # Request JSON
                }
            )
            response.raise_for_status()
            raw_content = response.json()['choices'][0]['message']['content']
            # Extract JSON from within ```json``` markers
            json_match = re.search(r'```json\s*(.*?)\s*```', raw_content, re.DOTALL)
            if json_match:
                json_content = json_match.group(1)  # Get the content between the markers
                feedback = json.loads(json_content)
            else:
                # Fallback: Try parsing directly if no markers are found
                feedback = json.loads(raw_content)
        except requests.RequestException as e:
            return Response({"error": f"OpenRouter API failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except json.JSONDecodeError as e:
            print("JSON parsing error:", str(e))
            return Response({"error": "Invalid JSON response from AI"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(feedback, status=status.HTTP_200_OK)


class ResumeListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_at')
        serializer = ResumeSerializer(resumes, many=True)
        return Response({"resumes": serializer.data}, status=status.HTTP_200_OK)


class ResumeUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ResumeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Save the instance with the authenticated user
            resume = serializer.save(user=request.user)
            process_resume.delay(resume.id)
            return Response(ResumeSerializer(resume).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)