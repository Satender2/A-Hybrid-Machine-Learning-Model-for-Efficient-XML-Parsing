from django.db import models
from django.conf import settings
import os

class XMLFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='xml_files/')
    original_filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField(help_text="File size in bytes")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Profiling data
    total_elements = models.IntegerField(null=True, blank=True)
    max_depth = models.IntegerField(null=True, blank=True)
    total_attributes = models.IntegerField(null=True, blank=True)
    file_complexity = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return f"{self.original_filename} - {self.user.username}"
    
    def get_file_size_mb(self):
        return round(self.file_size / (1024 * 1024), 2)
    
    class Meta:
        db_table = 'xml_files'
        ordering = ['-uploaded_at']


class SystemConfig(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    processor_cores = models.IntegerField(default=4)
    available_memory = models.FloatField(help_text="Available memory in GB")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Config for {self.user.username}"
    
    class Meta:
        db_table = 'system_configs'
