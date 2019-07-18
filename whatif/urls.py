"""whatif URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls import url
from login import views as login_views
from upload import views as upload_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_views.dashboard, name='dashboard'),
    path('ajax_dashboard/', login_views.ajax_dashboard, name='ajax_dashboard'),
    path('profile/', login_views.profile, name='profile'),
    path('profile/', include('login.urls')),
    path('login/', login_views.user_login, name='login'),
    path('logout/', login_views.logout, name='logout'),
    path('signup/', login_views.signup, name='signup'),
    path('otp/', login_views.verify_otp, name='otp'),
    path('forgot_password/', login_views.forgot_password, name='forgot_password'),
    path('otp_verification/', login_views.otp_verification, name='otp_verification'),
    path('reset_password/', login_views.reset_password, name='reset_password'),
    path('upload/', upload_views.upload_csv, name='upload_csv'),
    path('whatifsearch/', upload_views.whatifsearch, name='whatifsearch'),
    path('detailspage/', upload_views.detailspage, name='detailspage'),
    path('priceoptimization/', upload_views.priceoptimization, name='priceoptimization'),
    path('setting/', upload_views.setting, name='setting'),
    path('categorydisplay/', upload_views.categorydisplay, name='categorydisplay'),
    path('promotion/', upload_views.promotion, name='promotion'),
    path('promotionnamedisplay/', upload_views.promotionnamedisplay, name='promotionnamedisplay'),
    path('productnamedisplay/', upload_views.productnamedisplay, name='productnamedisplay'),
    path('ajax_whatif_export/', upload_views.ajax_whatif_export, name='ajax_whatif_export'),
    path('execution/', upload_views.execution, name='execution'),
]
