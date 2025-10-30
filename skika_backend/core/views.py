from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import authenticate
from .models import User, Ward, Project, Report, Feedback, AuditLog, Notification
from .serializers import (
    UserSerializer, WardSerializer, ProjectSerializer,
    ReportSerializer, FeedbackSerializer, AuditLogSerializer, NotificationSerializer
)
import africastalking
from decouple import config
import uuid

# Initialize Africa's Talking
africastalking.initialize(
    username=config('AFRICASTALKING_USERNAME'),
    api_key=config('AFRICASTALKING_API_KEY')
)
sms = africastalking.SMS


# Authentication Views

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    phone = request.data.get('phone_number')
    password = request.data.get('password_hash')
    user = authenticate(request, phone_number=phone, password_hash=password)
    if user and user.is_active:
        refresh = RefreshToken.for_user(user)
        AuditLog.objects.create(
            user=user, action_type='login', table_name='user',
            record_id=user.id, description="User logged in"
        )
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_citizen(request):
    phone = request.data.get('phone_number')
    ward_name = request.data.get('ward')
    if not phone or not ward_name:
        return Response({'error': 'phone_number and ward required'}, status=status.HTTP_400_BAD_REQUEST)

    ward = Ward.objects.filter(name__iexact=ward_name).first()
    if not ward:
        return Response({'error': 'Invalid ward'}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        user, created = User.objects.get_or_create(
            phone_number=phone,
            defaults={'role': 'citizen', 'ward': ward_name}
        )
        if created:
            AuditLog.objects.create(
                user=user, action_type='create', table_name='user',
                record_id=user.id, description="Citizen registered via USSD"
            )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def ussd_menu(request):
    session_id = request.data.get('sessionId')
    phone = request.data.get('phoneNumber')
    text = request.data.get('text', '').strip()

    user = User.objects.filter(phone_number=phone).first()
    if not user:
        return Response({"USSResponse": "END Invalid user. Contact support."})

    response = ""
    if text == "":
        response = "CON Welcome to Skika\n1. Report Issue\n2. Track Report\n3. Give Feedback"
    elif text == "1":
        wards = Ward.objects.values_list('name', flat=True)
        ward_list = "\n".join([f"{i+1}. {w}" for i, w in enumerate(wards)])
        response = f"CON Select Ward:\n{ward_list}"
    elif text.startswith("1*"):
        parts = text.split("*")
        if len(parts) == 2:
            ward_idx = int(parts[1]) - 1
            ward = list(Ward.objects.all())[ward_idx] if 0 <= ward_idx < Ward.objects.count() else None
            if ward:
                request.session['ward'] = ward.name
                response = "CON Enter issue description:"
        elif len(parts) == 3:
            description = parts[2]
            ward = Ward.objects.get(name=request.session.get('ward'))
            with transaction.atomic():
                report = Report.objects.create(
                    citizen=user, ward=ward, category='other', description=description
                )
                msg = f"Report {report.ref_code} received. We are reviewing."
                Notification.objects.create(
                    recipient_phone=phone, message=msg, trigger_event='report_created'
                )
                sms.send(msg, [phone])
            response = f"END Thank you! Ref: {report.ref_code}"
    elif text == "2":
        response = "CON Enter your report reference (e.g., SKK-2025-001):"
    elif text.startswith("2*"):
        ref_code = text.split("*")[1]
        report = Report.objects.filter(ref_code=ref_code, citizen=user).first()
        if report:
            response = f"END Status: {report.get_status_display()}"
        else:
            response = "END Invalid reference"
    elif text == "3":
        response = "CON Enter report ref to rate (1-5):"
    elif text.startswith("3*"):
        ref_code, rating = text.split("*")[1:]
        report = Report.objects.filter(ref_code=ref_code, citizen=user).first()
        if report and report.status in ['resolved', 'closed']:
            Feedback.objects.update_or_create(
                report=report, citizen=user,
                defaults={'rating': int(rating)}
            )
            response = "END Thank you for your feedback!"
        else:
            response = "END Report not resolved yet."

    return Response({"USSResponse": response})






# ViewSets with RBAC

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'leader', 'superadmin']

class IsCitizen(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'citizen'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class WardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    permission_classes = [permissions.AllowAny]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'citizen':
            return self.queryset.filter(citizen=self.request.user)
        return self.queryset

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def update_status(self, request, pk=None):
        report = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Report.STATUS_CHOICES):
            old_status = report.status
            report.status = new_status
            report.save()
            AuditLog.objects.create(
                user=request.user, action_type='status_change',
                table_name='report', record_id=report.id,
                description=f"Status: {old_status} → {new_status}"
            )
            msg = f"Report {report.ref_code} is now {report.get_status_display()}."
            Notification.objects.create(
                recipient_phone=report.citizen.phone_number,
                message=msg, trigger_event='status_updated'
            )
            sms.send(msg, [report.citizen.phone_number])
            return Response({'message': 'Status updated and SMS sent'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'citizen':
            return self.queryset.filter(citizen=self.request.user)
        return self.queryset


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]