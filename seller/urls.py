from django.urls import path, re_path

from . import views


urlpatterns = [
    path('login/', views.login, name='seller-login'),
    path('register/', views.register, name='seller-registration'),
    path('register/<str:uid>/2FA/setup/', views.TwoFA, name='seller-2FA-setup'),
    re_path(r'^dashboard/(?P<seller>[\w@.\-+]+)/$', views.dashboard, name='seller-dashboard'),
    re_path(r'^logout/(?P<seller>[\w@.\-+]+)/$', views.logout, name='seller-logout'),
]
