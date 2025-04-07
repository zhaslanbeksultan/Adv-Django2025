# resumes/serializers.py
from marshmallow import Schema, fields, post_load
from rest_framework import serializers

from resumes.models import Resume

# class ResumeSerializer(Schema):
#     id = fields.Int(dump_only=True)
#     user = fields.Nested('UserSchema', dump_only=True)  # Nested schema for user
#     file = fields.Str(required=True)  # File path as string
#     title = fields.Str(allow_none=True)
#     extracted_data = fields.Dict(dump_only=True)  # Read-only
#     uploaded_at = fields.DateTime(dump_only=True)  # Read-only
#     processed = fields.Boolean(dump_only=True)  # Read-only
#
#     class UserSchema(Schema):
#         id = fields.Int()
#         username = fields.Str()
#
#     @post_load
#     def make_resume(self, data, **kwargs):
#         # Convert validated data to a Resume instance
#         return Resume(**data)
#
#     def to_representation(self, obj):
#         # Customize serialization from Resume model
#         data = super().dump(obj)
#         data['file'] = obj.file.path  # Convert FileField to path
#         return data

class ResumeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    file = serializers.FileField()
    file_name = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = ['id', 'user', 'file', 'file_name', 'title', 'extracted_data', 'uploaded_at', 'processed']
        read_only_fields = ['id', 'user', 'extracted_data', 'uploaded_at', 'processed']

    def get_file_name(self, obj):
        return obj.file.name.split('/')[-1] if obj.file else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['file'] = instance.file.url
        return representation