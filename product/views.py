from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from . import models
from django.contrib import messages
from pprint import pprint
from user.models import User

# Create your views here.
class ProductsList(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 9
    ordering = ['id']

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
                    f'Insufficient stock for {amount_cart}x for the product "{product_name}". Added {variation_stock}x to your cart!'
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
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
        )
        variation_id = self.request.GET.get('vid')
        
        if not variation_id:
            return redirect(http_referer)
        
        if not self.request.session.get('cart'):
            return redirect(http_referer)
        
        if variation_id not in self.request.session['cart']:
            return redirect(http_referer)
        
        cart = self.request.session['cart'][variation_id]
        
        messages.success(
            self.request,
            f'Product {cart["product_name"]} {cart["variation_name"]} removed from your cart!'
        )
        
        del self.request.session['cart'][variation_id]
        self.request.session.save()
        
        return redirect(http_referer)

class Cart(View):
    def get(self, *args, **kwargs):
        context = {
            'cart': self.request.session.get('cart', {})
        }
        return render(self.request, 'product/cart.html', context)

class PurchaseSummary(View):
    def get(self, *args, **kwargs):
        
        if not self.request.user.is_authenticated:
            return redirect('user:create')
        
        user = User.objects.filter(user=self.request.user).exists()
        
        if not user:
            messages.error(
                self.request,
                'User has no profile.'
            )
            return redirect('user:create')
        
        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Your cart is empty.'
            )
            return redirect('product:list')
                    
        context = {
            'user': self.request.user,
            'cart': self.request.session['cart']
        }
                
        return render(self.request, 'product/purchasesummary.html', context) 
