from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from . import models
from django.contrib import messages

# Create your views here.
class ProductsList(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 1

class ProductDetail(DetailView):
    model = models.Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

class AddToCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER', reverse('product:list'))
        id_variation = self.request.GET.get('vid')
        
        if not id_variation:
            messages.error(
                self.request,
                'This product does not exist!'
            )
            return redirect(http_referer)
        
        variation = get_object_or_404(models.Option, id=id_variation)
        
        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()
            
        cart = self.request.session['cart']
        
        if id_variation in cart:
            ...
        else:
            ...
        
        return HttpResponse('Add to cart')
        

class RemoveFromCart(View):
    pass

class Cart(View):
    pass

class Finalize(View):
    pass
