from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from . import models
from django.contrib import messages
from pprint import pprint

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
        # del cart when needed
        # if self.request.session.get('cart'):
        #     del self.request.session['cart']
        #     self.request.session.save()
            
        http_referer = self.request.META.get('HTTP_REFERER', reverse('product:list'))
        variation_id = self.request.GET.get('vid')
        
        if not variation_id:
            messages.error(
                self.request,
                'This product does not exist!'
            )
            return redirect(http_referer)
        
        variation = get_object_or_404(models.Option, id=variation_id)
        variation_stock = variation.stock
        product = variation.product
        
        product_id = product.id
        product_name = product.name
        variation_name = variation.name or ''
        price_unitary = variation.price
        price_unitary_promotional = variation.price_promotional
        amount = 1
        slug = product.slug
        image =product.image
        
        if image:
            image = image.name
        else:
            image =''
        
        if variation.stock < 1:
            messages.error(
                self.request,
                'Insufficient stock'
            )
            return redirect(http_referer)
                    
        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()
            
        cart = self.request.session['cart']
        
        if variation_id in cart:
            
            amount_cart = cart[variation_id]['amount']
            amount_cart += 1
            
            if variation_stock < amount_cart:
                messages.warning(
                    self.request,
                    f'Insufficient stock for {amount_cart}x the product "{product_name}". Added {variation_stock}x to your cart!'
                )
                
                amount_cart = variation_stock
                
            cart[variation_id]['amount'] = amount_cart
            cart[variation_id]['price_quantitave'] = price_unitary * amount_cart
            cart[variation_id]['price_quantitave_promotional'] = price_unitary_promotional * amount_cart
                
        else:
            
            cart[variation_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_name': variation_name,
                'variation_id': variation_id,
                'price_unitary': price_unitary,
                'price_unitary_promotional': price_unitary_promotional,
                'price_quantitative': price_unitary,
                'price_quantitative_promotional': price_unitary_promotional,
                'amount': 1,
                'slug': slug,
                'image': image,
            }
            
        self.request.session.save()
        
        messages.success(
            self.request,
            f"Product {product_name} {variation_name} added to you cart {cart[variation_id]['amount']}x."
        )
        
        return redirect(http_referer)
        

class RemoveFromCart(View):
    pass

class Cart(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'product/cart.html')

class Finalize(View):
    pass
