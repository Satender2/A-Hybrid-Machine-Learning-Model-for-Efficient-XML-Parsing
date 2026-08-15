from django.db import models
from django.conf import settings
from xml_profiler.models import XMLFile
from core.models import XMLParser, MLModel

class ParsingResult(models.Model):
    xml_file = models.ForeignKey(XMLFile, on_delete=models.CASCADE)
    selected_parser = models.ForeignKey(XMLParser, on_delete=models.SET_NULL, null=True)
    ml_model_used = models.ForeignKey(MLModel, on_delete=models.SET_NULL, null=True)
    
    # Performance metrics
    parsing_time = models.FloatField(help_text="Time in seconds")
    memory_used = models.FloatField(help_text="Memory in MB")
    cpu_usage = models.FloatField(help_text="CPU usage percentage")
    
    # Prediction confidence
    prediction_confidence = models.FloatField(default=0.0)
    
    # Generated code
    optimized_code = models.TextField(blank=True, null=True)
    code_file_path = models.CharField(max_length=255, blank=True, null=True)
    
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Result for {self.xml_file.original_filename}"
    
    class Meta:
        db_table = 'parsing_results'
        ordering = ['-created_at']


class ParserPerformanceData(models.Model):
    xml_file = models.ForeignKey(XMLFile, on_delete=models.CASCADE)
    parser = models.ForeignKey(XMLParser, on_delete=models.CASCADE)
    
    # Input features
    file_size_mb = models.FloatField()
    total_elements = models.IntegerField()
    max_depth = models.IntegerField()
    processor_cores = models.IntegerField()
    
    # Performance outputs
    parsing_time = models.FloatField()
    memory_usage = models.FloatField()
    efficiency_score = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.parser.name} - {self.xml_file.original_filename}"
    
    class Meta:
        db_table = 'parser_performance_data'
