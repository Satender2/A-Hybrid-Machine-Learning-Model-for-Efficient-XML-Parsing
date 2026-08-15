from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Avg
from core.models import XMLParser, MLModel
from .models import TrainingDataset, SystemLog
from .forms import XMLParserForm, TrainingDatasetUploadForm, ModelTrainingForm
from parser_optimizer.ml_predictor import ParserMLPredictor
from xml_profiler.models import XMLFile
from parser_optimizer.models import ParsingResult
import os

def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Statistics
    total_users = XMLFile.objects.values('user').distinct().count()
    total_parsers = XMLParser.objects.filter(is_active=True).count()
    total_uploads = XMLFile.objects.count()
    total_parsings = ParsingResult.objects.count()
    
    # ML Model stats
    active_models = MLModel.objects.filter(is_active=True)
    
    # Recent logs
    recent_logs = SystemLog.objects.all()[:10]
    
    # Parser usage
    parser_usage = ParsingResult.objects.values(
        'selected_parser__name'
    ).annotate(count=Count('id')).order_by('-count')
    
    context = {
        'total_users': total_users,
        'total_parsers': total_parsers,
        'total_uploads': total_uploads,
        'total_parsings': total_parsings,
        'active_models': active_models,
        'recent_logs': recent_logs,
        'parser_usage': parser_usage
    }
    
    return render(request, 'admin_panel/dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def parser_management(request):
    parsers = XMLParser.objects.all()
    
    if request.method == 'POST':
        form = XMLParserForm(request.POST)
        if form.is_valid():
            form.save()
            SystemLog.objects.create(
                user=request.user,
                log_type='SUCCESS',
                message=f'New parser added: {form.cleaned_data["name"]}',
                module='Parser Management'
            )
            messages.success(request, 'Parser added successfully!')
            return redirect('admin_panel:parser_management')
    else:
        form = XMLParserForm()
    
    context = {
        'parsers': parsers,
        'form': form
    }
    
    return render(request, 'admin_panel/parser_management.html', context)


@login_required
@user_passes_test(is_admin)
def edit_parser(request, pk):
    parser = get_object_or_404(XMLParser, pk=pk)
    
    if request.method == 'POST':
        form = XMLParserForm(request.POST, instance=parser)
        if form.is_valid():
            form.save()
            messages.success(request, 'Parser updated successfully!')
            return redirect('admin_panel:parser_management')
    else:
        form = XMLParserForm(instance=parser)
    
    context = {
        'form': form,
        'parser': parser
    }
    
    return render(request, 'admin_panel/edit_parser.html', context)


@login_required
@user_passes_test(is_admin)
def delete_parser(request, pk):
    parser = get_object_or_404(XMLParser, pk=pk)
    
    if request.method == 'POST':
        parser_name = parser.name
        parser.delete()
        SystemLog.objects.create(
            user=request.user,
            log_type='WARNING',
            message=f'Parser deleted: {parser_name}',
            module='Parser Management'
        )
        messages.success(request, 'Parser deleted successfully!')
    
    return redirect('admin_panel:parser_management')


@login_required
@user_passes_test(is_admin)
def training_management(request):
    datasets = TrainingDataset.objects.all().order_by('-uploaded_at')
    ml_models = MLModel.objects.all().order_by('-trained_at')
    
    if request.method == 'POST':
        dataset_form = TrainingDatasetUploadForm(request.POST, request.FILES)
        
        if dataset_form.is_valid():
            dataset = dataset_form.save(commit=False)
            dataset.uploaded_by = request.user
            dataset.filename = request.FILES['dataset_file'].name
            dataset.save()
            
            # Count records in CSV
            import pandas as pd
            try:
                df = pd.read_csv(dataset.dataset_file.path)
                dataset.total_records = len(df)
                dataset.save()
            except:
                pass
            
            SystemLog.objects.create(
                user=request.user,
                log_type='SUCCESS',
                message=f'Training dataset uploaded: {dataset.filename}',
                module='ML Training'
            )
            
            messages.success(request, 'Training dataset uploaded successfully!')
            return redirect('admin_panel:training')
    else:
        dataset_form = TrainingDatasetUploadForm()
        training_form = ModelTrainingForm()
    
    context = {
        'datasets': datasets,
        'ml_models': ml_models,
        'dataset_form': dataset_form,
        'training_form': ModelTrainingForm()
    }
    
    return render(request, 'admin_panel/training.html', context)


@login_required
@user_passes_test(is_admin)
def train_model(request):
    if request.method == 'POST':
        form = ModelTrainingForm(request.POST)
        
        if form.is_valid():
            model_type = form.cleaned_data['model_type']
            dataset = form.cleaned_data['dataset']
            
            # Initialize predictor
            predictor = ParserMLPredictor()
            
            try:
                # Train models
                results = predictor.train_and_save_models(dataset.dataset_file.path)
                
                # Save model records
                if model_type in ['ANN', 'BOTH']:
                    MLModel.objects.create(
                        name=f'ANN Model - {dataset.filename}',
                        model_type='ANN',
                        model_file='core/ml_models/ann_model.pkl',
                        accuracy=results['ann_metrics']['accuracy'],
                        precision=results['ann_metrics']['precision'],
                        recall=results['ann_metrics']['recall'],
                        f1_score=results['ann_metrics']['f1_score'],
                        is_active=True
                    )
                
                if model_type in ['SVM', 'BOTH']:
                    MLModel.objects.create(
                        name=f'SVM Model - {dataset.filename}',
                        model_type='SVM',
                        model_file='core/ml_models/svm_model.pkl',
                        accuracy=results['svm_metrics']['accuracy'],
                        precision=results['svm_metrics']['precision'],
                        recall=results['svm_metrics']['recall'],
                        f1_score=results['svm_metrics']['f1_score'],
                        is_active=True
                    )
                
                SystemLog.objects.create(
                    user=request.user,
                    log_type='SUCCESS',
                    message=f'ML models trained successfully using {dataset.filename}',
                    module='ML Training'
                )
                
                messages.success(request, f'{model_type} model(s) trained successfully!')
                
            except Exception as e:
                SystemLog.objects.create(
                    user=request.user,
                    log_type='ERROR',
                    message=f'Model training failed: {str(e)}',
                    module='ML Training'
                )
                messages.error(request, f'Training failed: {str(e)}')
            
            return redirect('admin_panel:training')
    
    return redirect('admin_panel:training')


@login_required
@user_passes_test(is_admin)
def system_logs(request):
    logs = SystemLog.objects.all().order_by('-created_at')
    
    context = {
        'logs': logs
    }
    
    return render(request, 'admin_panel/logs.html', context)
