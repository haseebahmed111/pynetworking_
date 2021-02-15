from django.urls import path,include
from . import views
urlpatterns = [
#    path('dashboard/',views.dashboard,name='dashboard'),
    path('send_balance',views.send_balance_exchanger,name='send_balance_exchanger'),
    path('pending_list', views.pending_list, name='pending_list'),
    path('send/<pk>', views.send_pending, name='send_pending_balance'),
]