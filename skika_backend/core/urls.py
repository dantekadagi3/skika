# SKIKA/skika_backend/core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    dashboard_login, register_citizen, ussd_menu,
    DashboardUserViewSet, CitizenViewSet, WardViewSet, ProjectViewSet,
    ReportViewSet, FeedbackViewSet, AuditLogViewSet, NotificationViewSet,
    get_translations, translate_field, dashboard_stats
)
from .views import sentiment_analysis

router = DefaultRouter()
router.register(r'dashboard-users', DashboardUserViewSet)
router.register(r'citizens', CitizenViewSet)
router.register(r'wards', WardViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'audit-logs', AuditLogViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Authentication endpoints
    path('dashboard-login/', dashboard_login, name='dashboard_login'),
    path('register-citizen/', register_citizen, name='register_citizen'),
    
    # USSD endpoint
    path('ussd/', ussd_menu, name='ussd_menu'),
    
    # Translation and utility endpoints
    path('translations/', get_translations, name='get_translations'),
    path('translate/', translate_field, name='translate_field'),
    path('dashboard-stats/', dashboard_stats, name='dashboard_stats'),
    path('sentiment/', sentiment_analysis, name='sentiment_analysis'),
]