import time
import stripe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from carts.models import Cart
from .models import Order
from .utils import id_generator
from accounts.forms import UserAddressForm
from accounts.models import UserAddress
from django.conf import settings
from django.contrib import messages
# Create your views here.


try:
    stripe_pub = settings.STRIPE_PUBLISHABLE_KEY
    stripe_secret = settings.STRIPE_SECRET_KEY
except Exception as e:
    print(str(e))
    raise NotImplementedError(str(e))

stripe.api_key = stripe_secret


def orders(request):
    context = {}
    template = 'orders/user.html'
    return render(request, template, context)

@login_required
def checkout(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
        # print(cart)
    except:
        the_id = None
        return HttpResponseRedirect(reverse('view_cart'))

    try:
        new_order = Order.objects.get(cart=cart)
    except Order.DoesNotExist:
        new_order = Order()
        new_order.cart = cart
        new_order.user = request.user
        new_order.order_id = id_generator()
        new_order.save()
    except:
        new_order = None
        return HttpResponseRedirect(reverse('view_cart'))
        
    final_amount = 0
    if new_order is not None:
        new_order.sub_total = cart.total
        final_amount = new_order.get_final_amount()
        new_order.save()

    try:
        address_added = request.GET.get('address_added')
    except:
        address_added = None

    if address_added is None:
        address_form = UserAddressForm()
    else:
        address_form = None
    
    current_address = UserAddress.objects.filter(user=request.user)
    billing_address = UserAddress.objects.get_billing_address(user=request.user)
    # print(billing_address)

    ##1 Add shipping address
    ##2 Add billing address
    ##3 Add and run credit card

    if request.method == 'POST':
        try:
            user_stripe = request.user.userstripe.stripe_id
            customer = stripe.Customer.retrieve(user_stripe)
            # print(customer)
        except:
            customer = None
            pass
        if customer is not None:
            # shipping_a = request.POST['shipping_address']
            # billing_a = request.POST['billing_address']
            token = request.POST['stripeToken']
            card = stripe.Customer.create_source(customer.stripe_id, source=token)
            # print(card)
            charge = stripe.Charge.create(
                amount=int(final_amount * 100),
                currency="usd",
                source="tok_visa",
                description="My First Test Charge For %s" %(request.user.username),
                )
            if charge['captured']:
                new_order.status = 'Finished'
                new_order.save()
                del request.session['cart_id']
                del request.session['items_total']
                messages.success(request, 'Thank you for your order! It has been completed')
                return HttpResponseRedirect(reverse('user_orders'))

    context = {
        'address_form':address_form,
        'current_address':current_address,
        'billing_address':billing_address,
        'stripe_pub':stripe_pub,
        'order':new_order,
        }
    template = 'orders/checkout.html'
    return render(request, template, context)