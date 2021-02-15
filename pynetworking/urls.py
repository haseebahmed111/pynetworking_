"""pynetworking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from member import views as member_views
from django.views.generic.base import RedirectView
from main import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('member/',include('member.urls')),
    path('exchanger/',include('exchanger.urls')),
    path('referral/<username>', member_views.register_by_referral, name='register_by_referral'),
    path('contact_us/',member_views.contact_us,name='contact_us'),
    path('favicon.ico',RedirectView.as_view(url='/static/favicon/favicon.ico'), name='favicon'),
    path('marketing_plan',main_views.marketing_plan,name='marketing_plan')


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
