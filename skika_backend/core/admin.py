from django.contrib import admin
from django.utils.html import format_html
from .models import DashboardUser, Citizen, Ward, Project, Report, Feedback, AuditLog, Notification


@admin.register(DashboardUser)
class DashboardUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'get_full_name', 'role', 'ward', 'is_active', 'date_joined')
    list_filter = ('role', 'ward', 'is_active', 'date_joined')
    search_fields = ('phone_number', 'first_name', 'last_name', 'email')
    readonly_fields = ('date_joined', 'last_login')

    def get_full_name(self, obj):
        return f"{obj.first_name or ''} {obj.last_name or ''}".strip() or "Dashboard User"
    get_full_name.short_description = "Name"


@admin.register(Citizen)
class CitizenAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'ward', 'created_at')
    list_filter = ('ward', 'created_at')
    search_fields = ('phone_number',)
    readonly_fields = ('created_at',)


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'constituency', 'county', 'population_estimate')
    search_fields = ('name', 'constituency')


class TranslationFieldsetMixin:
    """Mixin to show English and Swahili fields in fieldsets"""
    
    class Media:
        js = ('admin/js/translation_autofill.js',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin, TranslationFieldsetMixin):
    list_display = ('project_code', 'title_en', 'category_en', 'status_en', 'ward', 'created_by', 'created_at')
    list_filter = ('status_en', 'category_en', 'ward', 'created_at')
    search_fields = ('project_code', 'title_en', 'title_sw')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('project_code', 'ward', 'created_by')
        }),
        ('Title & Description', {
            'fields': (('title_en', 'title_sw'), ('description_en', 'description_sw'))
        }),
        ('Categories & Status (Auto-fill Swahili)', {
            'fields': (('category_en', 'category_sw'), ('status_en', 'status_sw')),
            'description': 'Select English options and Swahili will auto-fill when saved'
        }),
        ('Budget & Dates', {
            'fields': ('budget_allocated', 'budget_used', 'start_date', 'end_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin, TranslationFieldsetMixin):
    list_display = ('ref_code', 'citizen', 'ward', 'category_en', 'status_en', 'priority_level_en', 'created_at')
    list_filter = ('status_en', 'category_en', 'priority_level_en', 'ward', 'created_at')
    search_fields = ('ref_code', 'description', 'citizen__phone_number')
    readonly_fields = ('ref_code', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('ref_code', 'citizen', 'ward', 'project')
        }),
        ('Categories & Status (Auto-fill Swahili)', {
            'fields': (
                ('category_en', 'category_sw'), 
                ('status_en', 'status_sw'),
                ('priority_level_en', 'priority_level_sw')
            ),
            'description': 'Select English options and Swahili will auto-fill when saved'
        }),
        ('Description & Notes', {
            'fields': ('description', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_under_review', 'mark_action_taken']

    def mark_under_review(self, request, queryset):
        updated = queryset.update(status_en='under_review', status_sw='chini_ya_ukaguzi')
        self.message_user(request, f'{updated} reports marked as Under Review.')
    mark_under_review.short_description = "Mark selected as Under Review"

    def mark_action_taken(self, request, queryset):
        updated = queryset.update(status_en='action_taken', status_sw='hatua_imechukuliwa')
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
    list_display = ('recipient_phone', 'message_preview', 'status_en', 'trigger_event', 'sent_at')
    list_filter = ('status_en', 'trigger_event', 'created_at')
    search_fields = ('recipient_phone', 'message')
    readonly_fields = ('created_at', 'sent_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('recipient_phone', 'trigger_event')
        }),
        ('Message Content', {
            'fields': ('message',)
        }),
        ('Status (Auto-fill Swahili)', {
            'fields': (('status_en', 'status_sw'),),
            'description': 'Select English status and Swahili will auto-fill when saved'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'sent_at'),
            'classes': ('collapse',)
        })
    )

    def message_preview(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_preview.short_description = "Message"