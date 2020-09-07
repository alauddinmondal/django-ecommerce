from django.db import models
from products.models import Product, Variation
from django.urls import reverse

# Create your models here.


class Cart(models.Model):
    total = models.DecimalField(decimal_places=2, max_digits=100, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "Cart id: %s" %(self.id)



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.CASCADE)
    line_total = models.DecimalField(default=10.99, max_digits=100, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField(default=1)
    notes = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        try:
            return str(self.cart.id)
        except:
            return self.product.title

    # def get_absolute_url(self):
    #     # return '/products/product-%s' %(self.pk)
    #     return reverse("update_cart", kwargs={'slug':self.slug})

        

