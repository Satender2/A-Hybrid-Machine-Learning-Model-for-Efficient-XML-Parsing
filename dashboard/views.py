from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from xml_profiler.models import XMLFile
from parser_optimizer.models import ParsingResult
from datetime import datetime, timedelta

@login_required
def home(request):
    user = request.user
    
    # User statistics
    total_uploads = XMLFile.objects.filter(user=user).count()
    total_parsings = ParsingResult.objects.filter(xml_file__user=user).count()
    
    # Recent uploads
    recent_uploads = XMLFile.objects.filter(user=user).order_by('-uploaded_at')[:5]
    
    # Recent results
    recent_results = ParsingResult.objects.filter(
        xml_file__user=user
    ).select_related('xml_file', 'selected_parser', 'ml_model_used').order_by('-created_at')[:5]
    
    # Average parsing time
    avg_parsing_time = ParsingResult.objects.filter(
        xml_file__user=user, success=True
    ).aggregate(Avg('parsing_time'))['parsing_time__avg'] or 0
    
    # Parser usage statistics
    parser_stats = ParsingResult.objects.filter(
        xml_file__user=user
    ).values('selected_parser__name').annotate(count=Count('id')).order_by('-count')
    
    context = {
        'total_uploads': total_uploads,
        'total_parsings': total_parsings,
        'recent_uploads': recent_uploads,
        'recent_results': recent_results,
        'avg_parsing_time': round(avg_parsing_time, 4),
        'parser_stats': parser_stats
    }
    
    return render(request, 'dashboard/home.html', context)
