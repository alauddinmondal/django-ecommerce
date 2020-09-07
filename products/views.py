from django.shortcuts import render, Http404
from .models import Product, ProductImage
from marketing.models import MarketingMessage, Slider

# Create your views here.

def search(request):
    try:
        q = request.GET.get('q')
    except:
        q = None
    if q:
        products = Product.objects.filter(title__icontains=q)
        context = {'query':q, 'products':products}
        template = 'products/results.html'
        return render(request, template, context)
    else:
        context = {}
        template = 'products/home.html'
        return render(request, template, context)


def home(request):
    sliders = Slider.objects.all_featured()
    products = Product.objects.all()
    marketing_message = MarketingMessage.objects.all()[0]
    context = {
        'products':products, 
        'marketing_message':marketing_message,
        'sliders':sliders
        }
    
    template = 'products/home.html'
    return render(request, template, context)

def all(request):
    products = Product.objects.all()
    context = {'products':products}

    template = 'products/all.html'
    return render(request, template, context)



def single(request, pk):
    try:
        product = Product.objects.get(id=pk)
        image = ProductImage.objects.filter(product=product)
        context = {'product':product, 'image':image}
        template = 'products/single.html'
        return render(request, template, context)
    except:
        raise Http404
        

    

    