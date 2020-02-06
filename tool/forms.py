from django import forms
from .models import Document
from .models import Configuration
from .models import CrawlerConfiguration
from .models import Crawlerurl

# Linking forms to models
class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)

class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        fields = ('title','topics','dateFrom', 'dateUntil', 'documents')

class CrawlerConfigurationForm(forms.ModelForm):
    class Meta:
        model = CrawlerConfiguration
        fields = ('title','stopAfter', 'amountSites','dateFrom', 'dateUntil', 'urls')

class CrawlerurlForm(forms.ModelForm):
    class Meta:
        model = Crawlerurl
        fields = ('title',)