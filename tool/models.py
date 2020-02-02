
from django.db import models



class Document(models.Model):
    title = models.CharField(max_length=100, blank=True)
    extension = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.title


class Configuration(models.Model):
    title = models.CharField(max_length=100, blank=True)
    topics = models.CharField(max_length=100,blank=True)
    dateFrom = models.CharField(max_length=100, blank=True)
    dateUntil = models.CharField(max_length=100, blank=True)
    documents = models.ManyToManyField(Document, blank=True)


    


    def __str__(self):
        return self.title


    