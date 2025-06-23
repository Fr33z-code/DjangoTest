from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from app1 import views
from rest_framework.routers import DefaultRouter
from app1.api_views import ProductViewSet, CartViewSet, OrderViewSet, CategoryViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup_view, name='signup'),
    path('accounts/login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('profile/', views.profile_view, name='profile'),
    path('create_order_for_user/', views.create_order_for_user, name='create_order_for_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.catalog, name='catalog'),
    path('add-to-cart-ajax/', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('cart/', views.view_cart, name='view_cart'),
    path('delete_from_cart/<int:product_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('yandex/callback/', views.yandex_callback, name='yandex_callback'),
    path('cart/update_item/', views.update_cart_item, name='update_cart_item'),
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
