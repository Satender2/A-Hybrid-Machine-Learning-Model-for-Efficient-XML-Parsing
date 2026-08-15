from django import forms
from core.models import XMLParser, MLModel
from .models import TrainingDataset

class XMLParserForm(forms.ModelForm):
    class Meta:
        model = XMLParser
        fields = ['name', 'description', 'best_for', 'memory_efficient', 'speed_efficient', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'best_for': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'memory_efficient': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'speed_efficient': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TrainingDatasetUploadForm(forms.ModelForm):
    class Meta:
        model = TrainingDataset
        fields = ['dataset_file', 'description']
        widgets = {
            'dataset_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.csv'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dataset description...'
            })
        }
    
    def clean_dataset_file(self):
        file = self.cleaned_data.get('dataset_file')
        
        if file:
            if not file.name.endswith('.csv'):
                raise forms.ValidationError('Only CSV files are allowed.')
            
            if file.size > 52428800:  # 50MB
                raise forms.ValidationError('Dataset file cannot exceed 50MB.')
        
        return file


class ModelTrainingForm(forms.Form):
    MODEL_CHOICES = [
        ('ANN', 'Artificial Neural Network'),
        ('SVM', 'Support Vector Machine'),
        ('BOTH', 'Train Both Models')
    ]
    
    model_type = forms.ChoiceField(
        choices=MODEL_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='BOTH'
    )
    
    dataset = forms.ModelChoiceField(
        queryset=TrainingDataset.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select training dataset"
    )
