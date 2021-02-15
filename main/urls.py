from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('sendmail', views.mail_test,name='testmail'),
    #path('mail', views.mail_template, name='mail'),
    path('rewards',views.promo_list,name='rewards'),
    path('rewards/claim/<pk>', views.promo_1, name='claim_reward'),

]