from django.db import models
from django.conf import settings

class XMLParser(models.Model):
    PARSER_CHOICES = (
        ('DOM', 'DOM Parser'),
        ('SAX', 'SAX Parser'),
        ('StAX', 'StAX Parser'),
        ('ElementTree', 'ElementTree Parser'),
        ('lxml', 'LXML Parser'),
    )
    
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    best_for = models.TextField(help_text="Scenarios where this parser performs best")
    memory_efficient = models.BooleanField(default=False)
    speed_efficient = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'xml_parsers'


class MLModel(models.Model):
    MODEL_TYPES = (
        ('ANN', 'Artificial Neural Network'),
        ('SVM', 'Support Vector Machine'),
    )
    
    name = models.CharField(max_length=100)
    model_type = models.CharField(max_length=10, choices=MODEL_TYPES)
    model_file = models.CharField(max_length=255, help_text="Path to model file")
    accuracy = models.FloatField(default=0.0)
    precision = models.FloatField(default=0.0)
    recall = models.FloatField(default=0.0)
    f1_score = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=False)
    trained_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.model_type})"
    
    class Meta:
        db_table = 'ml_models'
