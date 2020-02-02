from django import forms
from .models import Document
from .models import Configuration

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)

class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        fields = ('title','topics','dateFrom', 'dateUntil', 'documents')