from rest_framework import serializers
from .models import DashboardUser, Citizen, Ward, Project, Report, Feedback, AuditLog, Notification
from .translations import get_swahili_translation


class DashboardUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class CitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizen
        fields = '__all__'


class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        
    def validate(self, data):
        """Auto-fill Swahili fields if not provided"""
        # Auto-fill category_sw if category_en is provided but category_sw is not
        if 'category_en' in data and 'category_sw' not in data:
            data['category_sw'] = get_swahili_translation('category', data['category_en'])
            
        # Auto-fill status_sw if status_en is provided but status_sw is not
        if 'status_en' in data and 'status_sw' not in data:
            data['status_sw'] = get_swahili_translation('project_status', data['status_en'])
            
        return data


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ('ref_code',)
        
    def validate(self, data):
        """Auto-fill Swahili fields if not provided"""
        # Auto-fill category_sw if category_en is provided but category_sw is not
        if 'category_en' in data and 'category_sw' not in data:
            data['category_sw'] = get_swahili_translation('category', data['category_en'])
            
        # Auto-fill status_sw if status_en is provided but status_sw is not
        if 'status_en' in data and 'status_sw' not in data:
            data['status_sw'] = get_swahili_translation('report_status', data['status_en'])
            
        # Auto-fill priority_level_sw if priority_level_en is provided but priority_level_sw is not
        if 'priority_level_en' in data and 'priority_level_sw' not in data:
            data['priority_level_sw'] = get_swahili_translation('priority', data['priority_level_en'])
            
        return data


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        
    def validate(self, data):
        """Auto-fill Swahili status if not provided"""
        if 'status_en' in data and 'status_sw' not in data:
            status_mapping = {
                'pending': 'inayosubiri',
                'sent': 'imetumwa',
                'failed': 'imeshindwa'
            }
            data['status_sw'] = status_mapping.get(data['status_en'], 'inayosubiri')
        return data