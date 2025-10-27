from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ReportViewSet, ProjectViewSet, FeedbackViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'feedback', FeedbackViewSet)

urlpatterns = router.urls