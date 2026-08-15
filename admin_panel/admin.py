from django.contrib import admin
from .models import TrainingDataset, SystemLog

@admin.register(TrainingDataset)
class TrainingDatasetAdmin(admin.ModelAdmin):
    list_display = ['filename', 'total_records', 'uploaded_by', 'uploaded_at']
    list_filter = ['uploaded_at', 'uploaded_by']
    search_fields = ['filename', 'description']
    readonly_fields = ['uploaded_at']
    ordering = ['-uploaded_at']
    
    fieldsets = (
        ('Dataset Information', {
            'fields': ('uploaded_by', 'dataset_file', 'filename')
        }),
        ('Details', {
            'fields': ('total_records', 'description')
        }),
        ('Metadata', {
            'fields': ('uploaded_at',)
        })
    )


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ['log_type', 'module', 'message_preview', 'user', 'created_at']
    list_filter = ['log_type', 'module', 'created_at']
    search_fields = ['message', 'module', 'user__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'
    
    def has_add_permission(self, request):
        return False  # Logs are generated automatically
