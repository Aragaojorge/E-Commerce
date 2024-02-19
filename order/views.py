from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from product.models import Option
from utils import utils
from .models import Order, ItemOrder

# If not loggeg in, it goes to create user
class DispachLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('user:create')
        return super().dispatch(*args, **kwargs)
    
    # Access only your own orders, avoiding access others user orders
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        
        return qs  
    
class Pay(DispachLoginRequiredMixin, DetailView):
    template_name = 'order/pay.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'

    

class SaveOrder(View):
    
    template_name = 'order/pay.html'
    
    def get(self, *args, **kwargs):
    
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Please log in!'
            )
            return redirect('user:create')
        
        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Empty cart!'
            )
            return redirect('product:list')
        
        cart = self.request.session.get('cart')
        cart_option_ids = [v for v in cart]
        db_options = list(
            Option.objects.select_related('product').filter(id__in=cart_option_ids)
        )
        print(db_options)
        for option in db_options:
            vid = str(option.id) 
            stock = option.stock
            qty_cart = cart[vid]['amount']
            price_unit = cart[vid]['price_unitary']
            price_unit_promo = cart[vid]['price_unitary_promotional']
            
            error_msg_stock = ''
            
            if stock < qty_cart:
                cart[vid]['amount'] = stock
                cart[vid]['price_quantitative'] = stock * price_unit
                cart[vid]['price_quantitative_promotional'] = stock * price_unit_promo
                
                error_msg_stock = 'Insufficiente stock for some product in your cart. '\
                                  'We reduce the amoutn of those products. Please, check which product were affected!'

            if error_msg_stock:
                messages.error(
                    self.request,
                    error_msg_stock
                )
                self.request.session.save()
                return redirect('product:cart')
            
        qty_total_cart = utils.cart_total_qty(cart)
        value_total_cart = utils.cart_totals(cart)
        
        order = Order(
            user=self.request.user,
            total=value_total_cart,
            qty_total=qty_total_cart,
            status='C',
        )
        
        order.save()
        
        ItemOrder.objects.bulk_create([
            ItemOrder(
                order=order,
                product=v['product_name'],
                product_id=v['product_id'],
                option=v['option'],
                id_order=v['option_id'],
                price=v['price_quantitative'],
                price_promotional=v['price_quantitative_promotional'],
                quantity=v['amount'],
                image=v['image'],
                
            ) for v in cart.values()
        ])
            
        del self.request.session['cart']
        return redirect(
            reverse(
                'order:pay',
                kwargs={
                    'pk': order.pk
                }
            )
        )

class Detail(DispachLoginRequiredMixin, DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'order/detail.html'
    pk_url_kwarg = 'pk'

class List(DispachLoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order/list.html'
    paginate_by = 10
    ordering = ['-id']