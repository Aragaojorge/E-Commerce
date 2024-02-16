from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse

# Create your views here.
class Pay(View):
    def get(sel, *args, **kwargs):
        return HttpResponse('Pay')
    
class SaveOrder(View):
    pass

class Detail(View):
    pass