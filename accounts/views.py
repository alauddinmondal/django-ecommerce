import re
from django.shortcuts import render, redirect, HttpResponseRedirect, Http404, reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .forms import LoginForm, RegistrationForm, UserAddressForm
from .models import EmailConfirmed, UserDefaultAddress



def logout_view(request):
    logout(request)
    messages.success(request, '<strong>Successfully logged out</strong>, please feel free to <a href="%s">login</a> again' %(reverse('auth_login')), extra_tags='safe, abc')
    messages.warning(request, 'There\'s a warning.')
    messages.error(request, 'There\'s a error.')
    return HttpResponseRedirect('%s'%(reverse('auth_login')))
    

def login_view(request):
    form = LoginForm(request.POST or None)
    btn = 'Login'
    if form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, 'Successfully logged in, welcome back')
        # user.emailconfirmed.active_user_email()
        return redirect('home')

    context = {
        'form':form,
        'btn':btn,
    }
    return render(request, 'form.html', context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    btn = 'Join'
    if form.is_valid():
        new_user = form.save(commit=False)
        # new_user.first_name = 'Alauddin'
        new_user.save()
        messages.success(request, 'Successfully registered, please confirm your email now')
        return HttpResponseRedirect('/')
        
        # username = request.POST['username']
        # password = request.POST['password']
        # user = authenticate(username=username, password=password)
        # login(request, user)

    context = {
        'form':form,
        'btn':btn,
    }
    return render(request, 'form.html', context)


SHA1_RE = re.compile('^[a-f0-9]{40}$')

def activation_view(request, activation_key):
    if SHA1_RE.search(activation_key):
        print('Activation key is real')
        try:
            instance = EmailConfirmed.objects.get(activation_key=activation_key)
        except EmailConfirmed.DoesNotExist:
            instance = None
            messages.success(request, 'There was an error with your request.')
            return HttpResponseRedirect('/')
        
        if instance is not None and not instance.confirmed:
            page_message = 'Confirmation successful, Welcome!'
            instance.confirmed = True
            instance.activation_key = 'Confirmed'
            instance.save()
            messages.success(request, 'Successfully confirmed, please login')
        elif instance is not None and instance.confirmed:
            page_message = 'User already confirmed'
            messages.success(request, 'already confirmed.')
        else:
            page_message = ""

        context = {'page_message':page_message}
        return render(request, 'accounts/activation_complete.html', context)
    else:
        raise Http404


def add_user_address(request):
    print(request.GET)
    try:
        next_page = request.GET.get('next')
    except:
        next_page = None
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid:
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            is_default = form.cleaned_data['default']
            if is_default:
                default_address, created = UserDefaultAddress.objects.get_or_create(user=request.user)
                default_address.shipping = new_address
                default_address.save()

            if next_page is not None:
                return HttpResponseRedirect(reverse(str(next_page))+'?address_added=True')
    else:
        raise Http404

    