"""
URL configuration for POBucket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login, name='buyer-login'),
    path('register/', views.register, name='buyer-registration'),
    path('verify-email/<str:id>/', views.email_verification, name='buyer-email-verification'),
    path('logout/<str:buyer>/', views.logout, name='buyer-logout'),
    path('profile/<str:buyer>/', views.profile, name='buyer-profile'),
    path('portal/<str:buyer>/', views.portal, name='buyer-portal'),
    path('password/reset/<str:buyer>/', views.password_reset, name='buyer-password-reset'),
    path('history/<str:buyer>/', views.history, name='buyer-history'), # TODO: Test route change later
    path('portal/bidding/<str:buyer>/<str:pid>/', views.place_bid, name='place-bid'),
    path('payment/<str:buyer>/<str:pid>/', views.payment, name='buyer-payment'),
    path('payment/verify/', views.verify_payment, name='verify-payment'),
    # path('payment/success/thank-you/', views.payment_success, name='payment-success'),
]
