from django.contrib import admin
from .models import XMLParser, MLModel

@admin.register(XMLParser)
class XMLParserAdmin(admin.ModelAdmin):
    list_display = ['name', 'memory_efficient', 'speed_efficient', 'is_active', 'created_at']
    list_filter = ['memory_efficient', 'speed_efficient', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    ordering = ['name']
    
    fieldsets = (
        ('Parser Information', {
            'fields': ('name', 'description', 'best_for')
        }),
        ('Performance Characteristics', {
            'fields': ('memory_efficient', 'speed_efficient')
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )


@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_type', 'accuracy', 'precision', 'f1_score', 'is_active', 'trained_at']
    list_filter = ['model_type', 'is_active', 'trained_at']
    search_fields = ['name']
    list_editable = ['is_active']
    ordering = ['-trained_at']
    readonly_fields = ['trained_at', 'updated_at']
    
    fieldsets = (
        ('Model Information', {
            'fields': ('name', 'model_type', 'model_file')
        }),
        ('Performance Metrics', {
            'fields': ('accuracy', 'precision', 'recall', 'f1_score')
        }),
        ('Status', {
            'fields': ('is_active', 'trained_at', 'updated_at')
        })
    )
