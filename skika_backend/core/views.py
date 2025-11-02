from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import authenticate
from .models import DashboardUser, Citizen, Ward, Project, Report, Feedback, AuditLog, Notification
from .serializers import (
    DashboardUserSerializer, CitizenSerializer, WardSerializer, ProjectSerializer,
    ReportSerializer, FeedbackSerializer, AuditLogSerializer, NotificationSerializer
)
from .translations import get_swahili_translation, get_display_translation
import africastalking
from decouple import config
import uuid
try:
    # Prefer transformer-based analyzer when available
    from .utils.sentiment_transformer import analyze_sentiment
except Exception:
    # Fall back to the lightweight lexicon analyzer
    from .utils.sentiment import analyze_sentiment

# Initialize Africa's Talking
africastalking.initialize(
    username=config('AFRICASTALKING_USERNAME'),
    api_key=config('AFRICASTALKING_API_KEY')
)
sms = africastalking.SMS


# Authentication Views

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def dashboard_login(request):
    """Login for dashboard users (admins, leaders)"""
    phone = request.data.get('phone_number')
    password = request.data.get('password')
    user = authenticate(request, username=phone, password=password)
    if user and user.is_active and isinstance(user, DashboardUser):
        refresh = RefreshToken.for_user(user)
        AuditLog.objects.create(
            user=user, action_type='login', table_name='dashboard_user',
            record_id=user.id, description="Dashboard user logged in"
        )
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': DashboardUserSerializer(user).data
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_citizen(request):
    """Register a citizen via USSD or API"""
    phone = request.data.get('phone_number')
    ward_name = request.data.get('ward')
    if not phone or not ward_name:
        return Response({'error': 'phone_number and ward required'}, status=status.HTTP_400_BAD_REQUEST)

    ward = Ward.objects.filter(name__iexact=ward_name).first()
    if not ward:
        return Response({'error': 'Invalid ward'}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        citizen, created = Citizen.objects.get_or_create(
            phone_number=phone,
            defaults={'ward': ward}
        )
        if created:
            # Create audit log entry using a dashboard user if available
            admin_user = DashboardUser.objects.filter(role='admin').first()
            if admin_user:
                AuditLog.objects.create(
                    user=admin_user, action_type='create', table_name='citizen',
                    record_id=citizen.id, description=f"Citizen registered via USSD: {phone}"
                )
        return Response(CitizenSerializer(citizen).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def ussd_menu(request):
    """Handle USSD menu interactions with bilingual support"""
    session_id = request.data.get('sessionId')
    phone = request.data.get('phoneNumber')
    text = request.data.get('text', '').strip()
    
    # Get or create citizen
    citizen = Citizen.objects.filter(phone_number=phone).first()
    if not citizen:
        # Auto-register citizen with default ward
        default_ward = Ward.objects.first()
        if default_ward:
            citizen = Citizen.objects.create(phone_number=phone, ward=default_ward)
        else:
            return Response({"USSResponse": "END Service unavailable. Contact support."})

    response = ""
    if text == "":
        response = ("CON Welcome to Skika - Karibu Skika\n"
                   "1. Report Issue - Ripoti Tatizo\n"
                   "2. Track Report - Fuatilia Ripoti\n"
                   "3. Give Feedback - Toa Maoni")
    elif text == "1":
        wards = Ward.objects.values_list('name', flat=True)
        ward_list = "\n".join([f"{i+1}. {w}" for i, w in enumerate(wards)])
        response = f"CON Select Ward - Chagua Kata:\n{ward_list}"
    elif text.startswith("1*"):
        parts = text.split("*")
        if len(parts) == 2:
            try:
                ward_idx = int(parts[1]) - 1
                wards_list = list(Ward.objects.all())
                if 0 <= ward_idx < len(wards_list):
                    ward = wards_list[ward_idx]
                    request.session['ward_id'] = str(ward.id)
                    response = ("CON Categories - Aina za Matatizo:\n"
                              "1. Infrastructure - Miundombinu\n"
                              "2. Health - Afya\n"
                              "3. Education - Elimu\n"
                              "4. Security - Usalama\n"
                              "5. Other - Mengine")
                else:
                    response = "END Invalid ward selection"
            except (ValueError, IndexError):
                response = "END Invalid selection"
        elif len(parts) == 3:
            try:
                category_idx = int(parts[2]) - 1
                categories = ['infrastructure', 'health', 'education', 'security', 'other']
                if 0 <= category_idx < len(categories):
                    request.session['category'] = categories[category_idx]
                    response = "CON Enter issue description - Elezea tatizo:"
                else:
                    response = "END Invalid category"
            except (ValueError, IndexError):
                response = "END Invalid selection"
        elif len(parts) == 4:
            description = parts[3]
            ward_id = request.session.get('ward_id')
            category = request.session.get('category', 'other')
            
            if ward_id and description:
                try:
                    ward = Ward.objects.get(id=ward_id)
                    with transaction.atomic():
                        report = Report.objects.create(
                            citizen=citizen, 
                            ward=ward, 
                            category_en=category,
                            # Swahili auto-fills via model save method
                            description=description
                        )
                        # Bilingual message
                        msg_en = f"Report {report.ref_code} received. We are reviewing."
                        msg_sw = f"Ripoti {report.ref_code} imepokelewa. Tunakagua."
                        msg = f"{msg_en} / {msg_sw}"
                        
                        Notification.objects.create(
                            recipient_phone=phone, message=msg, trigger_event='report_created'
                        )
                        try:
                            sms.send(msg, [phone])
                        except Exception as e:
                            # Log SMS failure but don't fail the request
                            pass
                    
                    response = f"END Thank you! Ref: {report.ref_code}\nAsante! Namba: {report.ref_code}"
                except Ward.DoesNotExist:
                    response = "END Invalid ward. Please try again."
            else:
                response = "END Invalid input. Please try again."
    elif text == "2":
        response = "CON Enter report reference - Ingiza namba ya ripoti\n(e.g., SKK-2025-001):"
    elif text.startswith("2*"):
        ref_code = text.split("*")[1]
        report = Report.objects.filter(ref_code=ref_code, citizen=citizen).first()
        if report:
            status_en = report.status_en or report.category_en  # fallback
            status_sw = get_display_translation('report_status', status_en)
            response = f"END Status: {status_en} / Hali: {status_sw}"
        else:
            response = "END Invalid reference / Namba si sahihi"
    elif text == "3":
        response = "CON Enter report ref to rate (1-5) - Ingiza namba ya ripoti ili kukadiria (1-5):"
    elif text.startswith("3*"):
        try:
            parts = text.split("*")
            ref_code = parts[1]
            rating = int(parts[2]) if len(parts) > 2 else None
            
            if rating and 1 <= rating <= 5:
                report = Report.objects.filter(ref_code=ref_code, citizen=citizen).first()
                if report and report.status_en in ['resolved', 'closed']:
                    Feedback.objects.update_or_create(
                        report=report, citizen=citizen,
                        defaults={'rating': rating}
                    )
                    response = "END Thank you for your feedback! / Asante kwa maoni yako!"
                else:
                    response = "END Report not resolved yet / Ripoti bado haijatatuliwa"
            else:
                response = "CON Invalid rating. Enter 1-5 - Kadirio si sahihi. Ingiza 1-5:"
        except (ValueError, IndexError):
            response = "END Invalid input / Ingizo si sahihi"

    return Response({"USSResponse": response})






# ViewSets with RBAC

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'leader', 'superadmin']

class IsCitizen(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'citizen'


class DashboardUserViewSet(viewsets.ModelViewSet):
    queryset = DashboardUser.objects.all()
    serializer_class = DashboardUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class CitizenViewSet(viewsets.ModelViewSet):
    queryset = Citizen.objects.all()
    serializer_class = CitizenSerializer
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
        # Citizens can only see their own reports
        if hasattr(self.request.user, 'role') and self.request.user.role in ['citizen']:
            return self.queryset.filter(citizen__phone_number=self.request.user.phone_number)
        # Dashboard users can see all reports
        return self.queryset

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def update_status(self, request, pk=None):
        """Update report status with bilingual SMS notification"""
        report = self.get_object()
        new_status_en = request.data.get('status_en') or request.data.get('status')
        new_status_sw = request.data.get('status_sw')
        
        # Validate English status
        valid_statuses = [choice[0] for choice in Report.STATUS_CHOICES_EN]
        if new_status_en not in valid_statuses:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Auto-fill Swahili if not provided
        if not new_status_sw:
            new_status_sw = get_swahili_translation('report_status', new_status_en)
        
        old_status_en = report.status_en
        old_status_sw = report.status_sw
        
        # Update both fields
        report.status_en = new_status_en
        report.status_sw = new_status_sw
        report.save()
        
        # Create audit log
        AuditLog.objects.create(
            user=request.user, action_type='status_change',
            table_name='report', record_id=report.id,
            description=f"Status: {old_status_en}→{new_status_en} | {old_status_sw}→{new_status_sw}"
        )
        
        # Send bilingual SMS notification
        status_display_en = dict(Report.STATUS_CHOICES_EN).get(new_status_en, new_status_en)
        status_display_sw = get_display_translation('report_status', new_status_en)
        
        msg_en = f"Report {report.ref_code} is now {status_display_en}."
        msg_sw = f"Ripoti {report.ref_code} sasa ni {status_display_sw}."
        msg = f"{msg_en} / {msg_sw}"
        
        Notification.objects.create(
            recipient_phone=report.citizen.phone_number,
            message=msg, trigger_event='status_updated'
        )
        
        try:
            sms.send(msg, [report.citizen.phone_number])
            return Response({
                'message': 'Status updated and bilingual SMS sent',
                'status_en': new_status_en,
                'status_sw': new_status_sw
            })
        except Exception as e:
            return Response({
                'message': 'Status updated but SMS failed',
                'error': str(e),
                'status_en': new_status_en,
                'status_sw': new_status_sw
            })


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter based on user type
        if hasattr(self.request.user, 'role') and self.request.user.role in ['citizen']:
            return self.queryset.filter(citizen__phone_number=self.request.user.phone_number)
        return self.queryset


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


# Translation and Utility Views

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_translations(request):
    """Get available translations for choice fields"""
    from .translations import get_all_translations, DISPLAY_TRANSLATIONS
    
    return Response({
        'database_values': get_all_translations(),
        'display_values': DISPLAY_TRANSLATIONS,
        'supported_languages': ['en', 'sw'],
        'field_types': ['category', 'project_status', 'report_status', 'priority']
    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def translate_field(request):
    """Translate a specific field value from English to Swahili"""
    field_type = request.data.get('field_type')
    english_value = request.data.get('english_value')
    
    if not field_type or not english_value:
        return Response({
            'error': 'field_type and english_value required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    swahili_value = get_swahili_translation(field_type, english_value)
    display_value = get_display_translation(field_type, english_value)
    
    return Response({
        'field_type': field_type,
        'english_value': english_value,
        'swahili_value': swahili_value,
        'display_value': display_value
    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def sentiment_analysis(request):
    """Analyze sentiment for a provided text string.

    Request JSON: {"text": "..."}
    Response: {
      "text": "...",
      "sentiment": {"score": float, "label": str, ...}
    }
    """
    text = request.data.get('text') or ''
    if text is None or text == '':
        return Response({'error': 'text is required'}, status=status.HTTP_400_BAD_REQUEST)

    result = analyze_sentiment(text)

    return Response({
        'text': text,
        'sentiment': result
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics with bilingual labels"""
    stats = {
        'reports': {
            'total': Report.objects.count(),
            'by_status_en': {},
            'by_status_sw': {},
            'by_category_en': {},
            'by_category_sw': {},
        },
        'citizens': Citizen.objects.count(),
        'projects': Project.objects.count(),
        'wards': Ward.objects.count(),
    }
    
    # Report statistics by status
    for choice in Report.STATUS_CHOICES_EN:
        status_en = choice[0]
        count = Report.objects.filter(status_en=status_en).count()
        stats['reports']['by_status_en'][status_en] = count
        
        status_sw = get_swahili_translation('report_status', status_en)
        stats['reports']['by_status_sw'][status_sw] = count
    
    # Report statistics by category  
    for choice in Report.CATEGORY_CHOICES_EN:
        category_en = choice[0]
        count = Report.objects.filter(category_en=category_en).count()
        stats['reports']['by_category_en'][category_en] = count
        
        category_sw = get_swahili_translation('category', category_en)
        stats['reports']['by_category_sw'][category_sw] = count
    
    return Response(stats)