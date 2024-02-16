from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
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
                'profileform' : forms.ProfileForm(data=self.request.POST or None, instance=self.profile)
            }
        else:
            self.context = {        
            'userform': forms.UserForm(data=self.request.POST or None),
            'profileform' : forms.ProfileForm(data=self.request.POST or None)
        }
            
        self.userform = self.context['userform']
        self.profileform = self.context['profileform']
        
        if self.request.user.is_authenticated:
            self.template_name = 'user/update.html'
            
        self.renderize = render(self.request, self.template_name, self.context)
        
    def get(self, *args, **kwargs):
        return self.renderize


class Create(BaseProfile):
    def post(self, *args, **kwargs):
        
        if not self.userform.is_valid() or not self.profileform.is_valid():
            messages.error(
                self.request,
                'There are errors in your registration form. Please check if all fields are filled in correctly.'
            )
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
            
            if not self.profile:
                self.profileform.cleaned_data['user'] = user
                profile = models.User(**self.profileform.cleaned_data)
                profile.save()
                
            else:
                profile = self.profileform.save(commit=False)
                profile.user = user
                profile.save()
        
        # New user
        else:
            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()
            
            profile = self.profileform.save(commit=False)
            profile.user = user
            profile.save()
            
        if password:
            authenticaty = authenticate(
                self.request,
                username=user,
                password=password
            )
            
            if authenticaty:
                login(self.request, user=user)
            
        self.request.session['cart'] = self.cart        
        self.request.session.save()
        
        messages.success(
            self.request,
            'Your registration was created/updated successfully!'
        )
        
        messages.success(
            self.request,
            'You are logged in and you can finalize your purchase!'
        )
        
        return redirect('product:cart')
        return self.renderize

class Update(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Update')

class Login(View):
    def post(self, *args, **kwargs):
        
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        
        if not username or not password:
            messages.error(
                self.request,
                'Invalid username/password.'
            )   
            return redirect('user:create')     
        
        user = authenticate(self.request, username=username, password=password)    
        
        if not user:
            
            messages.error(
                self.request,
                'Invalid username/password.'
            )   
            return redirect('user:create')
            
        login(self.request, user=user)
        
        messages.success(
            self.request,
            'You are logged in and you can finalize your purchase!'
        )
        
        return redirect('product:cart')

class Logout(View):
    def get(self, *args, **kwargs):
        cart = copy.deepcopy(self.request.session.get('cart'))
        
        logout(self.request)
        
        self.request.session['cart'] = cart
        self.request.session.save()
        
        return redirect('product:list')
