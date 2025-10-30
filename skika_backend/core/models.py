# SKIKA/skika_backend/core/models.py
import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
import africastalking
from decouple import config

# Initialize Africa's Talking
africastalking.initialize(
    username=config('AFRICASTALKING_USERNAME'),
    api_key=config('AFRICASTALKING_API_KEY')
)
sms = africastalking.SMS


class Ward(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    constituency = models.CharField(max_length=100, default='Gatundu North')
    county = models.CharField(max_length=100, default='Kiambu')
    population_estimate = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ward'
        unique_together = ('name', 'constituency')

    def __str__(self):
        return self.name


# 1. User
class User(models.Model):
    ROLE_CHOICES = [
        ('citizen', 'Citizen'),
        ('admin', 'Admin'),
        ('leader', 'Leader'),
        ('superadmin', 'Super Admin'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')
    # ward = models.CharField(max_length=100, blank=True, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    password_hash = models.TextField(blank=True, null=True)  # For JWT login
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f"{self.phone_number} ({self.get_role_display()})"





class Project(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('stalled', 'Stalled'),
    ]
    CATEGORY_CHOICES = [
        ('education', 'Education'),
        ('infrastructure', 'Infrastructure'),
        ('health', 'Health'),
        ('water', 'Water'),
        ('environment', 'Environment'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    budget_allocated = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    budget_used = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project'

    def __str__(self):
        return f"{self.project_code} - {self.title}"



class Report(models.Model):
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('under_review', 'Under Review'),
        ('action_taken', 'Action Taken'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    CATEGORY_CHOICES = [
        ('infrastructure', 'Infrastructure'),
        ('education', 'Education'),
        ('health', 'Health'),
        ('security', 'Security'),
        ('environment', 'Environment'),
        ('other', 'Other'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref_code = models.CharField(max_length=20, unique=True, blank=True)
    citizen = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    priority_level = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    admin_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'report'

    def save(self, *args, **kwargs):
        if not self.ref_code:
            import datetime
            year = datetime.datetime.now().year
            last = Report.objects.filter(ref_code__startswith=f"SKK-{year}").count()
            self.ref_code = f"SKK-{year}-{str(last + 1).zfill(3)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ref_code



class Feedback(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report = models.OneToOneField(Report, on_delete=models.CASCADE, related_name='feedback')
    # citizen = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_given')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feedback'

    def __str__(self):
        return f"Feedback on {self.report.ref_code}"


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('status_change', 'Status Change'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    table_name = models.CharField(max_length=100)
    record_id = models.UUIDField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_log'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} - {self.action_type} on {self.table_name}"



class Notification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]
    EVENT_CHOICES = [
        ('report_created', 'Report Created'),
        ('status_updated', 'Status Updated'),
        ('feedback_request', 'Feedback Request'),
        ('general_announcement', 'General Announcement'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient_phone = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    trigger_event = models.CharField(max_length=30, choices=EVENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notification'

    def __str__(self):
        return f"SMS to {self.recipient_phone} - {self.status}"



@receiver(post_save)
def log_model_changes(sender, instance, created, **kwargs):
    if sender in [User, Report, Project, Feedback]:
        action = 'create' if created else 'update'
        
        # Determine which user to log for different models
        if hasattr(instance, 'created_by'):
            log_user = instance.created_by
        elif hasattr(instance, 'citizen'):
            log_user = instance.citizen
        elif sender == User:
            log_user = instance  # For User model, log the user itself
        else:
            return  # Skip logging if we can't determine the user
        
        AuditLog.objects.create(
            user=log_user,
            action_type=action,
            table_name=sender._meta.db_table,
            record_id=instance.id,
            description=f"{action.capitalize()}d {sender.__name__}"
        )

@receiver(post_save, sender=Report)
def send_status_sms(sender, instance, created, **kwargs):
    if not created and instance.status != 'received':
        message = f"Report {instance.ref_code} is now '{instance.get_status_display()}'."
        Notification.objects.create(
            recipient_phone=instance.citizen.phone_number,
            message=message,
            trigger_event='status_updated'
        )
        try:
            sms.send(message, [instance.citizen.phone_number])
            Notification.objects.filter(message=message).update(status='sent', sent_at=timezone.now())
        except:
            Notification.objects.filter(message=message).update(status='failed')