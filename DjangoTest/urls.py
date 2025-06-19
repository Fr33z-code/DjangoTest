from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from app1 import views
from rest_framework.routers import DefaultRouter
from app1.api_views import ProductViewSet, CartViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

cart_list = CartViewSet.as_view({
    'get': 'list',
})

cart_add = CartViewSet.as_view({
    'post': 'add_item',
})

cart_update = CartViewSet.as_view({
    'put': 'update_item',
})

cart_delete = CartViewSet.as_view({
    'delete': 'delete_item',
})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup_view, name='signup'),
    path('accounts/login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.catalog, name='catalog'),
    path('add-to-cart-ajax/', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('cart', views.view_cart, name='view_cart'),
    path('delete_from_cart/<int:product_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('yandex/callback/', views.yandex_callback, name='yandex_callback'),
    path('api/', include(router.urls)),
    path('api/cart/', cart_list, name='cart-list'),
    path('api/cart/add/', cart_add, name='cart-add'),
    path('api/cart/update/', cart_update, name='cart-update'),
    path('api/cart/delete/', cart_delete, name='cart-delete'),
    path('place_order/', views.place_order, name='place_order')
]
