from django import forms
from .models import XMLFile, SystemConfig

class XMLFileUploadForm(forms.ModelForm):
    class Meta:
        model = XMLFile
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.xml',
                'id': 'fileInput'
            })
        }
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        
        if file:
            # Check file extension
            if not file.name.endswith('.xml'):
                raise forms.ValidationError('Only XML files are allowed.')
            
            # Check file size (max 100MB)
            if file.size > 104857600:
                raise forms.ValidationError('File size cannot exceed 100MB.')
        
        return file


class SystemConfigForm(forms.ModelForm):
    class Meta:
        model = SystemConfig
        fields = ['processor_cores', 'available_memory']
        widgets = {
            'processor_cores': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of CPU cores',
                'min': '1',
                'max': '128'
            }),
            'available_memory': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Available RAM in GB',
                'step': '0.1',
                'min': '0.5'
            })
        }
