from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View

# Create your views here.
class ProductsList(ListView):
    pass

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
