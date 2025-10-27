from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import User, Report, Project, Feedback
from .serializers import UserSerializer, ReportSerializer, ProjectSerializer, FeedbackSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import africastalking
from django.core.cache import cache
import time
import uuid
from django.db import transaction
from textblob import TextBlob

# Initialize Africa's Talking
africastalking.initialize(
    username="YOUR_USERNAME",
    api_key="YOUR_API_KEY"
)
sms = africastalking.SMS

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        with transaction.atomic():
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    ref_id = f"SKK-2025-{uuid.uuid4().hex[:6]}"
                    serializer.save(ref_id=ref_id, user_id=self.request.user.id, audit_trail=f"Created at {time.ctime()}")
                    cache.set(f"session_{ref_id}", serializer.data, timeout=300)
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(2 ** attempt)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        with transaction.atomic():
            report = self.get_object()
            status = request.data.get('status')
            if status in dict(Report.STATUS_CHOICES):
                report.status = status
                report.audit_trail += f"\nStatus updated to {status} at {time.ctime()}"
                report.save()
                sms.send(f"Report {report.ref_id} status updated to {status}", [report.user.phone_number])
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def ussd_menu(self, request):
        session_id = request.data.get('sessionId')
        text = request.data.get('text', 'default').strip()
        with transaction.atomic():
            response = "CON What would you like to do?\n1. Report Issue\n2. Suggest\n3. Track Report"
            if text == "1":
                response = "CON Enter issue description"
            elif text.startswith("1 "):
                description = text[2:]
                report = Report.objects.create(user_id=request.user.id, ward="Ward1", category="Issue", description=description)
                response = f"END Report {report.ref_id} submitted"
            elif text == "3":
                response = "CON Enter reference ID to track"
            elif text.startswith("3 "):
                ref_id = text[2:]
                report = Report.objects.filter(ref_id=ref_id).first()
                response = f"END Status: {report.status}" if report else "END Invalid reference ID"
            return Response({"USSResponse": response})

    @action(detail=False, methods=['get'])
    def sentiment_analysis(self, request):
        reports = Report.objects.all()
        sentiments = {r.id: TextBlob(r.description).sentiment.polarity for r in reports}
        return Response(sentiments)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()