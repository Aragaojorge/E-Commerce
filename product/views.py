from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from . import models

# Create your views here.
class ProductsList(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 1

class ProductDetail(View):
    pass

class AddToCart(View):
    pass

class RemoveFromCart(View):
    pass

class Cart(View):
    pass

class Finalize(View):
    pass
