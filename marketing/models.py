# import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class MarketingQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(active=True).filter(start_date__lt=timezone.now()).filter(end_date__gte=timezone.now())

class MarketingManager(models.Manager):
    def get_queryset(self):
        return MarketingQueryset(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def all_featured(self):
        return self.get_queryset().active().featured()

    def get_featured_item(self):
        try:
            self.get_queryset().active().featured()[0]
        except:
            None




class MarketingMessage(models.Model):
    message = models.CharField(max_length=120)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    start_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

    objects = MarketingManager()

    def __str__(self):
        return self.message[:12]
    
    class Meta:
        ordering = ['-start_date', '-end_date']

def slider_upload(instance, filename):
    return 'images/marketing/slider/%s' %(filename)

class Slider(models.Model):
    image = models.ImageField(upload_to=slider_upload)
    # image = models.FileField(upload_to=slider_upload)
    order = models.IntegerField(default=0)
    url_link = models.CharField(max_length=120, null=True, blank=True)
    header_text = models.CharField(max_length=120, null=True, blank=True)
    text = models.CharField(max_length=120, null=True, blank=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    start_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

    objects = MarketingManager()

    def __str__(self):
        return str(self.image)
    
    class Meta:
        ordering = ['order','-start_date', '-end_date']