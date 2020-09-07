from django.contrib import admin
from .models import UserStripe, EmailConfirmed, EmailMarketingSignUp, UserAddress, UserDefaultAddress

# Register your models here.

admin.site.register(UserStripe)
admin.site.register(EmailConfirmed)
admin.site.register(UserDefaultAddress)

class EmailMarketingSignUpAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'timestamp']
    class Meta:
        model = EmailMarketingSignUp

class UserAddressAdmin(admin.ModelAdmin):
    class Meta:
        model = UserAddress

admin.site.register(EmailMarketingSignUp, EmailMarketingSignUpAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
