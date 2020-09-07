from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.


class CartAmdin(admin.ModelAdmin):
    class Meta:
        model = Cart

admin.site.register(Cart, CartAmdin)
admin.site.register(CartItem)