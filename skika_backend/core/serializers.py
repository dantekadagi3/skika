from rest_framework import serializers
from .models import User, Report, Project, Feedback

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'role', 'ward', 'created_at']

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'ref_id', 'user', 'ward', 'category', 'description', 'status', 'created_at', 'updated_at', 'audit_trail']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'ward', 'description', 'created_at']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'report', 'satisfaction', 'comments', 'created_at']