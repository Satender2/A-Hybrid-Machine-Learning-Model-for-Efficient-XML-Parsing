from django.contrib import admin
from .models import XMLFile, SystemConfig

@admin.register(XMLFile)
class XMLFileAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'user', 'file_size_display', 'total_elements', 'max_depth', 'file_complexity', 'uploaded_at']
    list_filter = ['file_complexity', 'uploaded_at', 'user']
    search_fields = ['original_filename', 'user__username']
    readonly_fields = ['uploaded_at']
    ordering = ['-uploaded_at']
    
    fieldsets = (
        ('File Information', {
            'fields': ('user', 'file', 'original_filename', 'file_size')
        }),
        ('Profile Data', {
            'fields': ('total_elements', 'max_depth', 'total_attributes', 'file_complexity')
        }),
        ('Metadata', {
            'fields': ('uploaded_at',)
        })
    )
    
    def file_size_display(self, obj):
        return f"{obj.get_file_size_mb()} MB"
    file_size_display.short_description = 'File Size'


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    list_display = ['user', 'processor_cores', 'available_memory', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']
    ordering = ['-created_at']
