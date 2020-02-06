from django.contrib import admin
from tool import models
# Register your models here.
admin.site.register(models.Document)
admin.site.register(models.Configuration)
admin.site.register(models.Crawlingurls)
admin.site.register(models.CrawlerConfiguration)