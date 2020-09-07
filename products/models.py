# from django.db import models
from django.db import models
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=100, default=19.99)
    sale_price = models.DecimalField(decimal_places=2, max_digits=100, null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    class Meta:
        unique_together = ['title','slug']

    def get_absolute_url(self):
        # return '/products/product-%s' %(self.pk)
        return reverse("single_product", kwargs={'pk':self.pk})



    # def get_price(self):
    #     return self.price

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.FileField(upload_to='products/images/')
    featured = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.product.title




class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(active=True)
    def sizes(self):
        # return super(VariationManager, self).filter(category='size')
        return self.all().filter(category='size')

    def colors(self):
        # return super(VariationManager, self).filter(category='color')
        return self.all().filter(category='color')


VAR_CATEGORIES = (
    ('size', 'size'),
    ('color', 'color'),
    ('package', 'package'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default='size')
    title = models.CharField(max_length=120)
    image = models.ForeignKey(ProductImage, null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    objects = VariationManager()

    def __str__(self):
        return self.title
   
    
def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, instance.title, instance.slug)

pre_save.connect(slug_save, sender=Product)

