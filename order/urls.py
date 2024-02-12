from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.Pay._as_view(), name='pay'),
    path('closeorder/', views.CloseOrder._as_view(), name='closeorder'),
    path('detail/', views.Detail._as_view(), name='detail'),
]