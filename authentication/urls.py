from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('accounts/sign-up/',views.user_registration_view, name='sign-up'),
    path('accounts/account-activation/<str:uidb64>/<str:token>/', views.account_activation_view, name='account-activation'),
    path('login/', views.login_view, name='dologin'),
    path('logout/', views.logout_view, name='dologout'),
    path('dashboard/', views.index_view, name='dashboard'),

]
