from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
import copy

from . import models
from . import forms 

# Create your views here.
class BaseProfile(View):
    
    template_name = 'user/create.html'
    
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        
        self.cart = copy.deepcopy(self.request.session.get('cart', {}))
        
        self.profile = None
        
        if self.request.user.is_authenticated:     
            self.profile = models.User.objects.filter(user=self.request.user).first()
            
            self.context = {        
                'userform': forms.UserForm(data=self.request.POST or None, user=self.request.user, instance=self.request.user),
                'profileform' : forms.ProfileForm(data=self.request.POST or None)
            }
        else:
            self.context = {        
            'userform': forms.UserForm(data=self.request.POST or None),
            'profileform' : forms.ProfileForm(data=self.request.POST or None)
        }
            
        self.userform = self.context['userform']
        self.profileform = self.context['profileform']
            
        self.renderize = render(self.request, self.template_name, self.context)
        
    def get(self, *args, **kwargs):
        return self.renderize


class Create(BaseProfile):
    def post(self, *args, **kwargs):
        
        if not self.userform.is_valid() or not self.profileform.is_valid():
            return self.renderize
        
        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')
        
        # Logged user
        if self.request.user.is_authenticated:
            user = get_object_or_404(User, username=self.request.user.username)
            
            user.username = username
            
            if password:
                user.set_password(password)
                
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            
            user.save()
        
        # New user
        else:
            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()
            
            profile = self.profileform.save(commit=False)
            profile.user = user
            profile.save()
            
        self.request.session['cart'] = self.cart
        
        self.request.session.save()
        
        return self.renderize

class Update(View):
    pass

class Login(View):
    pass

class Logout(View):
    pass
