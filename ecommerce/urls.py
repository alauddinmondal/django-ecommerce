"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from products import views as products_view
from carts import views as cart_view
from carts import views as remove_from_cart
from orders import views as checkout_views
from accounts import views as accounts_views
from marketing import views as marketingviews
# from accounts import views as login_view
# from accounts import views as register_view
# from orders import views as order_views



admin.autodiscover()
# from carts import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', products_view.home, name='home'),
    path('s/', products_view.search, name='search'),   
    path('products/', products_view.all, name='products'),
    path('products/product/<str:pk>/', products_view.single, name='single_product'),
    
    path('carts/<str:id>/', cart_view.remove_from_cart, name='remove_from_cart'),
    path('carts/', cart_view.view_cart, name='view_cart'),
    path('cart/<str:pk>/', cart_view.add_to_cart, name='add_to_cart'),
    path('checkout/', checkout_views.checkout, name='checkout'),
    path('orders/', checkout_views.orders, name='user_orders'),

    path('ajax/dismiss_marketing_message/', marketingviews.dismiss_marketing_message, name='dismiss_marketing_message'),
    path('ajax/email_signup/', marketingviews.email_signup, name='ajax_email_signup'),
    path('ajax/add_user_address/', accounts_views.add_user_address, name='ajax_add_user_address'),

    path('accounts/logout/', accounts_views.logout_view, name='auth_logout'),
    path('accounts/login/', accounts_views.login_view, name='auth_login'),
    path('accounts/register/', accounts_views.registration_view, name='auth_register'),
    path('accounts/activate/<str:activation_key>', accounts_views.activation_view, name='activation_view'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
