from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from app1 import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup_view, name='signup'),
    path('accounts/login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout')
]
