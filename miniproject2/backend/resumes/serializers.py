from rest_framework import serializers

from resumes.models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'user', 'file', 'title', 'extracted_data', 'uploaded_at', 'processed']
        read_only_fields = ['user', 'extracted_data', 'uploaded_at', 'processed']