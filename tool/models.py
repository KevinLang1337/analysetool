
from django.db import models


# Represents documents uploaded by the user
class Document(models.Model):
    title = models.CharField(max_length=100, blank=True)
    extension = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to='documents/')
    userID = models.IntegerField(blank=True, null=True)
    dateField = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.title


# Represents URLs for crawling added by the user
class Crawlerurl(models.Model):
    title = models.CharField(max_length=300, blank=True)
    userID = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

# Represents Configurations for Webcrawler
class CrawlerConfiguration(models.Model):
    title = models.CharField(max_length=100, blank=True)
    stopAfter = models.CharField(max_length=100, blank=True)
    amountSites = models.CharField(max_length=100,blank=True)
    dateFrom = models.CharField(max_length=100, blank=True)
    dateUntil = models.CharField(max_length=100, blank=True)
    urls = models.ManyToManyField(Crawlerurl, blank=True)
    userID = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

# Represents Configurations for Analysis
class Configuration(models.Model):
    title = models.CharField(max_length=100, blank=True)
    topics = models.CharField(max_length=100,blank=True)
    dateFrom = models.CharField(max_length=100, blank=True)
    dateUntil = models.CharField(max_length=100, blank=True)
    documents = models.ManyToManyField(Document, blank=True)
    userID = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title


    