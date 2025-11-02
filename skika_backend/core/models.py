import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import africastalking
from decouple import config

# Translation mappings for auto-fill functionality
TRANSLATION_MAPPINGS = {
    # Project/Report Categories (English -> Swahili)
    'category': {
        'education': 'elimu',
        'infrastructure': 'miundombinu', 
        'health': 'afya',
        'water': 'maji',
        'environment': 'mazingira',
        'security': 'usalama',
        'other': 'mengine'
    },
    # Project Status (English -> Swahili)
    'project_status': {
        'planned': 'imepangwa',
        'ongoing': 'inaendelea', 
        'completed': 'imekamilika',
        'stalled': 'imekwama'
    },
    # Report Status (English -> Swahili)
    'report_status': {
        'received': 'imepokelewa',
        'under_review': 'chini_ya_ukaguzi',
        'action_taken': 'hatua_imechukuliwa',
        'resolved': 'imetatuliwa',
        'closed': 'imefungwa'
    },
    # Priority (English -> Swahili)
    'priority': {
        'low': 'chini',
        'medium': 'kati', 
        'high': 'juu'
    }
}

def get_swahili_translation(field_type, english_value):
    """Get Swahili translation for English field value"""
    return TRANSLATION_MAPPINGS.get(field_type, {}).get(english_value, english_value)

# Africa's Talking
africastalking.initialize(
    username=config('AFRICASTALKING_USERNAME'),
    api_key=config('AFRICASTALKING_API_KEY')
)
sms = africastalking.SMS



class DashboardUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('leader', 'Leader'),
        ('superadmin', 'Super Admin'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, unique=True, db_index=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')
    ward = models.ForeignKey('Ward', on_delete=models.SET_NULL, null=True, blank=True, related_name='dashboard_users')

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'dashboard_user'
        verbose_name = 'Dashboard User'

    def __str__(self):
        return f"{self.phone_number} ({self.get_role_display()})"


class Citizen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, unique=True)
    ward = models.ForeignKey('Ward', on_delete=models.SET_NULL, null=True, blank=True, related_name='citizens')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'citizen'

    def __str__(self):
        return f"{self.phone_number} ({self.ward.name if self.ward else 'No Ward'})"



class Ward(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    constituency = models.CharField(max_length=100, default='Gatundu North')
    county = models.CharField(max_length=100, default='Kiambu')
    population_estimate = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'ward'
        ordering = ['name']

    def __str__(self):
        return self.name



class Project(models.Model):
    STATUS_CHOICES_EN = [
        ('planned', 'Planned'), ('ongoing', 'Ongoing'),
        ('completed', 'Completed'), ('stalled', 'Stalled')
    ]
    STATUS_CHOICES_SW = [
        ('imepangwa', 'Imeplanwa'), ('inaendelea', 'Inaendelea'),
        ('imekamilika', 'Imefanyika'), ('imekwama', 'Imekwama')
    ]
    CATEGORY_CHOICES_SW = [
        ('masomo', 'Elimu'), ('miundombinu', 'Miundombinu'),
        ('afya', 'Afya'), ('maji', 'Maji'),
        ('mazingira', 'Mazungira'), ('mengine', 'Mengine')
    ]
    CATEGORY_CHOICES_EN = [
        ('education', 'Education'), ('infrastructure', 'Infrastructure'),
        ('health', 'Health'), ('water', 'Water'),
        ('environment', 'Environment'), ('other', 'Other')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_code = models.CharField(max_length=20, unique=True)
    title_en = models.CharField(max_length=200)
    title_sw = models.CharField(max_length=200)
    description_en = models.TextField()
    description_sw = models.TextField()
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    category_en = models.CharField(max_length=20, choices=CATEGORY_CHOICES_EN)
    category_sw = models.CharField(max_length=20, choices=CATEGORY_CHOICES_SW)
    status_en = models.CharField(max_length=20, choices=STATUS_CHOICES_EN, default='planned')
    status_sw = models.CharField(max_length=20, choices=STATUS_CHOICES_SW, default='imepangwa')

    budget_allocated = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    budget_used = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(DashboardUser, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project'

    def save(self, *args, **kwargs):
        # Auto-fill Swahili fields based on English selections
        if self.category_en and not self.category_sw:
            self.category_sw = get_swahili_translation('category', self.category_en)
        
        if self.status_en and not self.status_sw:
            self.status_sw = get_swahili_translation('project_status', self.status_en)
            
        super().save(*args, **kwargs)

    def title(self, lang='en'):
        return self.title_sw if lang == 'sw' else self.title_en

    def description(self, lang='en'):
        return self.description_sw if lang == 'sw' else self.description_en

    def __str__(self):
        return f"{self.project_code} - {self.title()}"



class Report(models.Model):
    STATUS_CHOICES_EN = [
        ('received', 'Received'), ('under_review', 'Under Review'),
        ('action_taken', 'Action Taken'), ('resolved', 'Resolved'), ('closed', 'Closed')
    ]
    STATUS_CHOICES_SW = [
        ('imepokelewa', 'Imepokelewa'), ('chini_ya_kukaguzi', 'Chini ya Ukaguzi'),
        ('tathmini_imefanyika', 'Tathmini Imefanyika'), ('imetatuliwa', 'Imetatuliwa'), ('imefungwa', 'Imefungwa')
    ]


    CATEGORY_CHOICES_EN = [
        ('infrastructure', 'Infrastructure'), ('education', 'Education'),
        ('health', 'Health'), ('security', 'Security'),
        ('environment', 'Environment'), ('other', 'Other')
    ]
    CATEGORY_CHOICES_SW = [
        ('miundombinu', 'Miundombinu'), ('elimu', 'Elimu'),
        ('afya', 'Afya'), ('usalama', 'Usalama'),       
        ('mazingira', 'Mazungira'), ('mengine', 'Mengine')
    ]

    PRIORITY_CHOICES_EN = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    PRIORITY_CHOICES_SW = [('chini', 'Chini'), ('kati', 'Kati'), ('juu', 'Juu')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref_code = models.CharField(max_length=20, unique=True, blank=True)
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='reports')
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    category_en = models.CharField(max_length=20, choices=CATEGORY_CHOICES_EN)
    category_sw = models.CharField(max_length=20, choices=CATEGORY_CHOICES_SW)
    description = models.TextField()
    status_en = models.CharField(max_length=20, choices=STATUS_CHOICES_EN, default='received')
    status_sw = models.CharField(max_length=20, choices=STATUS_CHOICES_SW, default='received')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    priority_level_en = models.CharField(max_length=10, choices=PRIORITY_CHOICES_EN, default='medium')
    priority_level_sw = models.CharField(max_length=10, choices=PRIORITY_CHOICES_SW, default='kati')
    admin_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'report'

    def save(self, *args, **kwargs):
        # Generate ref_code if not present
        if not self.ref_code:
            import datetime
            year = datetime.datetime.now().year
            last = Report.objects.filter(ref_code__startswith=f"SKK-{year}").count()
            self.ref_code = f"SKK-{year}-{str(last + 1).zfill(3)}"
        
        # Auto-fill Swahili fields based on English selections
        if self.category_en and not self.category_sw:
            self.category_sw = get_swahili_translation('category', self.category_en)
        
        if self.status_en and not self.status_sw:
            self.status_sw = get_swahili_translation('report_status', self.status_en)
            
        if self.priority_level_en and not self.priority_level_sw:
            self.priority_level_sw = get_swahili_translation('priority', self.priority_level_en)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ref_code



class Feedback(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report = models.OneToOneField(Report, on_delete=models.CASCADE, related_name='feedback')
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feedback'


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'), ('update', 'Update'), ('delete', 'Delete'),
        ('status_change', 'Status Change'), ('login', 'Login')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(DashboardUser, on_delete=models.CASCADE, related_name='audit_logs')
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    table_name = models.CharField(max_length=100)
    record_id = models.UUIDField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_log'
        ordering = ['-timestamp']



class Notification(models.Model):
    STATUS_CHOICES_EN = [('pending', 'Pending'), ('sent', 'Sent'), ('failed', 'Failed')]
    STATUS_CHOICES_SW = [('inayosubiri', 'Inayosubiri'), ('imetumwa', 'Imetumwa'), ('imeshindwa', 'Imeshindwa')]
    EVENT_CHOICES = [
        ('report_created', 'Report Created'),
        ('status_updated', 'Status Updated'),
        ('feedback_request', 'Feedback Request')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient_phone = models.CharField(max_length=20)
    message = models.TextField()
    status_en = models.CharField(max_length=10, choices=STATUS_CHOICES_EN, default='pending')
    status_sw = models.CharField(max_length=10, choices=STATUS_CHOICES_SW, default='inayosubiri')   
    trigger_event = models.CharField(max_length=30, choices=EVENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notification'



# Signals

@receiver(post_save)
def log_admin_actions(sender, instance, created, **kwargs):
    if sender in [Project, Report] and hasattr(instance, 'created_by'):
        action = 'create' if created else 'update'
        AuditLog.objects.create(
            user=instance.created_by,
            action_type=action,
            table_name=sender._meta.db_table,
            record_id=instance.id,
            description=f"{action.capitalize()}d {sender.__name__}"
        )

@receiver(post_save, sender=Report)
def send_status_sms(sender, instance, created, **kwargs):
    if not created and instance.status != 'received':
        msg = f"Report {instance.ref_code} is now '{instance.get_status_display()}'."
        Notification.objects.create(
            recipient_phone=instance.citizen.phone_number,
            message=msg,
            trigger_event='status_updated'
        )
        try:
            sms.send(msg, [instance.citizen.phone_number])
            Notification.objects.filter(message=msg).update(status='sent', sent_at=timezone.now())
        except:
            Notification.objects.filter(message=msg).update(status='failed')