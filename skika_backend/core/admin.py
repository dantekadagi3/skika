from django.contrib import admin
from django.utils.html import format_html
from .models import User, Ward, Project, Report, Feedback, AuditLog, Notification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'get_name', 'role', 'ward', 'is_active', 'created_at')
    list_filter = ('role', 'ward', 'is_active', 'created_at')
    search_fields = ('phone_number', 'first_name', 'last_name', 'email')
    readonly_fields = ('created_at', 'updated_at')

    def get_name(self, obj):
        return f"{obj.first_name or ''} {obj.last_name or ''}".strip() or "Citizen"
    get_name.short_description = "Name"


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'constituency', 'county', 'population_estimate')
    search_fields = ('name', 'constituency')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_code', 'title', 'ward', 'status', 'budget_allocated', 'created_by')
    list_filter = ('status', 'category', 'ward', 'created_at')
    search_fields = ('project_code', 'title')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('ref_code', 'citizen', 'ward', 'category', 'status', 'priority_level', 'created_at')
    list_filter = ('status', 'category', 'priority_level', 'ward', 'created_at')
    search_fields = ('ref_code', 'description', 'citizen__phone_number')
    readonly_fields = ('ref_code', 'created_at', 'updated_at')
    actions = ['mark_under_review', 'mark_action_taken']

    def mark_under_review(self, request, queryset):
        updated = queryset.update(status='under_review')
        self.message_user(request, f'{updated} reports marked as Under Review.')
    mark_under_review.short_description = "Mark selected as Under Review"

    def mark_action_taken(self, request, queryset):
        updated = queryset.update(status='action_taken')
        self.message_user(request, f'{updated} reports marked as Action Taken.')
    mark_action_taken.short_description = "Mark selected as Action Taken"


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('report', 'citizen', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('report__ref_code', 'citizen__phone_number')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'table_name', 'timestamp')
    list_filter = ('action_type', 'table_name', 'timestamp')
    search_fields = ('user__phone_number', 'description')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient_phone', 'message_preview', 'status', 'trigger_event', 'sent_at')
    list_filter = ('status', 'trigger_event', 'created_at')
    search_fields = ('recipient_phone', 'message')
    readonly_fields = ('created_at', 'sent_at')

    def message_preview(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_preview.short_description = "Message"