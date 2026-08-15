from django.contrib import admin
from .models import ParsingResult, ParserPerformanceData

@admin.register(ParsingResult)
class ParsingResultAdmin(admin.ModelAdmin):
    list_display = ['xml_file', 'selected_parser', 'parsing_time', 'memory_used', 'prediction_confidence', 'success', 'created_at']
    list_filter = ['success', 'selected_parser', 'created_at']
    search_fields = ['xml_file__original_filename', 'selected_parser__name']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('File & Parser', {
            'fields': ('xml_file', 'selected_parser', 'ml_model_used')
        }),
        ('Performance Metrics', {
            'fields': ('parsing_time', 'memory_used', 'cpu_usage', 'prediction_confidence')
        }),
        ('Generated Code', {
            'fields': ('optimized_code', 'code_file_path'),
            'classes': ['collapse']
        }),
        ('Status', {
            'fields': ('success', 'error_message', 'created_at')
        })
    )
    
    def has_add_permission(self, request):
        return False  # Results are generated automatically


@admin.register(ParserPerformanceData)
class ParserPerformanceDataAdmin(admin.ModelAdmin):
    list_display = ['xml_file', 'parser', 'file_size_mb', 'parsing_time', 'memory_usage', 'efficiency_score', 'created_at']
    list_filter = ['parser', 'created_at']
    search_fields = ['xml_file__original_filename', 'parser__name']
    ordering = ['-created_at']
