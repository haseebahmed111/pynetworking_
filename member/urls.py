from django.urls import path,include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.register,name='signup'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('membership/',views.membership_page,name='membership'),
    path('membership/<mid>', views.buy_membership, name='buy_membership'),
    path('edit',views.edit_user,name='edit_profile'),
    path('logout',views.user_logout,name='logout'),
    path('referrals_info',views.referrals,name='referrals_info'),
    path('send/',views.send_balance,name='send_balance'),
    path('referrals_info/remove/<pk>', views.referral_remove, name='referral_remove'),
    path('transaction_history/', views.transaction_history, name='transaction_history'),

]