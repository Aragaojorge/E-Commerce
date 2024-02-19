from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from product.models import Option
from utils import utils
from .models import Order, ItemOrder

# Create your views here.
class Pay(View):
    
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
            Option.objects.select_related('product').filter(id_in=cart_option_ids)
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
                
                error_msg_stock = 'Insufficiente stock for some product in your cart'\
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
                option=v['option_name'],
                id_order=v['option_id'],
                price=v['price_quantitative'],
                price_promotional=v['price_quantitative_promotional'],
                quantity=v['amount'],
                image=v['image'],
                
            ) for v in cart.values()
        ])
            
        del self.request.session['cart']
        return redirect('order:list')
    
class SaveOrder(View):
    pass

class Detail(View):
    pass

class List(View):
    def get(self, *args, **kwargs):
        return HttpResponse('List')