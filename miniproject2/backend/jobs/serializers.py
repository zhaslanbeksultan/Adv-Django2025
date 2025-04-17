from rest_framework import serializers
from jobs.models import JobListing
from user_auth.models import User

class JobListingSerializer(serializers.ModelSerializer):
    posted_by = serializers.StringRelatedField(read_only=True)  # Displays username

    class Meta:
        model = JobListing
        fields = ['id', 'title', 'company', 'description', 'location', 'posted_by', 'created_at', 'is_active']
        extra_kwargs = {
            'id': {'read_only': True},
            'posted_by': {'read_only': True},
            'created_at': {'read_only': True},
        }

    def validate(self, attrs):
        # Custom validation for required fields
        if 'title' in attrs and len(attrs['title']) < 3:
            raise serializers.ValidationError({"title": "Title must be at least 3 characters long"})
        if 'company' in attrs and len(attrs['company']) < 2:
            raise serializers.ValidationError({"company": "Company name must be at least 2 characters long"})
        return attrs

    def create(self, validated_data):
        # Automatically set posted_by to the current user
        # user = self.context['request'].user
        user = User.objects.filter(id=18).first()
        # if user.role != 'recruiter':
        #     raise serializers.ValidationError({"error": "Only recruiters can create jobs"})
        job = JobListing.objects.create(posted_by=user, **validated_data)
        return job