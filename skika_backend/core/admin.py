from django.contrib import admin
from .models import User, Report, Project, Feedback

# Custom Admin for User Model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'role', 'ward', 'created_at')
    list_filter = ('role', 'ward', 'created_at')
    search_fields = ('phone_number', 'ward')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')  # Optimize queries if needed

# Custom Admin for Report Model
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('ref_id', 'user', 'ward', 'category', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'ward', 'created_at', 'updated_at')
    search_fields = ('ref_id', 'description', 'ward', 'category')
    ordering = ('-created_at',)
    readonly_fields = ('ref_id', 'created_at', 'updated_at', 'audit_trail')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # New object
            obj.audit_trail = f"Initial creation at {obj.created_at}"
        else:
            obj.audit_trail += f"\nUpdated at {obj.updated_at} by {request.user}"
        super().save_model(request, obj, form, change)

# Custom Admin for Project Model
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'ward', 'created_at')
    list_filter = ('ward', 'created_at')
    search_fields = ('name', 'description', 'ward')
    ordering = ('-created_at',)

# Custom Admin for Feedback Model
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('report', 'satisfaction', 'created_at')
    list_filter = ('satisfaction', 'created_at')
    search_fields = ('comments',)
    ordering = ('-created_at',)
