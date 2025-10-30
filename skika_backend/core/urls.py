# SKIKA/skika_backend/core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    login_view, register_citizen, ussd_menu,
    UserViewSet, WardViewSet, ProjectViewSet,
    ReportViewSet, FeedbackViewSet, AuditLogViewSet, NotificationViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'wards', WardViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'audit-logs', AuditLogViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view, name='login'),
    path('register-citizen/', register_citizen, name='register_citizen'),
    path('ussd/', ussd_menu, name='ussd_menu'),
]