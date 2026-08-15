from django.db import models
from django.conf import settings

class TrainingDataset(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dataset_file = models.FileField(upload_to='datasets/')
    filename = models.CharField(max_length=255)
    total_records = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.filename
    
    class Meta:
        db_table = 'training_datasets'


class SystemLog(models.Model):
    LOG_TYPES = (
        ('INFO', 'Information'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('SUCCESS', 'Success'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    log_type = models.CharField(max_length=20, choices=LOG_TYPES)
    message = models.TextField()
    module = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.log_type} - {self.module}"
    
    class Meta:
        db_table = 'system_logs'
        ordering = ['-created_at']
