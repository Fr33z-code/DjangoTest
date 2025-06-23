from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from app1.models import Cart, CartItem, Product, OrderItem, Order
from app1.serializers import CartItemSerializer, ProductSerializer, OrderSerializer, CategorySerializer


@extend_schema(tags=["Cart"])
class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Просмотр корзины",
        responses={200: CartItemSerializer(many=True)},
    )
    def list(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Добавить товар в корзину",
        request=CartItemSerializer,
        responses={200: CartItemSerializer},
    )
    @action(detail=False, methods=["post"])
    def add_item(self, request):
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"error": "product_id обязателен"}, status=400)

        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    @extend_schema(
        summary="Обновить количество товара в корзине",
        request=CartItemSerializer,
        responses={200: CartItemSerializer},
    )
    @action(detail=False, methods=["put"])
    def update_item(self, request):
        item_id = request.data.get("item_id")
        quantity = request.data.get("quantity")

        if not item_id or not quantity:
            return Response({"error": "item_id и quantity обязательны"}, status=400)

        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError
        except ValueError:
            return Response({"error": "Неверное количество"}, status=400)

        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.quantity = quantity
        item.save()
        serializer = CartItemSerializer(item)
        return Response(serializer.data)

    @extend_schema(
        summary="Удалить товар из корзины",
        request=CartItemSerializer,
        responses={200: dict},
    )
    @action(detail=False, methods=["delete"])
    def delete_item(self, request):
        item_id = request.data.get("item_id")
        if not item_id:
            return Response({"error": "item_id обязателен"}, status=400)

        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.delete()
        return Response({"success": True})

@extend_schema(tags=["Products"])
@extend_schema(
        summary="получение карточки конкретного товара",
        request=ProductSerializer,
        responses={200: dict},
    )
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(in_stock=True)
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        sort = self.request.query_params.get('sort')

        if category:
            qs = qs.filter(category=category)
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)

        if sort == 'price_asc':
            qs = qs.order_by('price')
        elif sort == 'price_desc':
            qs = qs.order_by('-price')

        return qs


@extend_schema(tags=["Order"])
class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Создание заказа",
        responses={201: OrderSerializer}
    )
    def create(self, request):
        user = request.user

        try:
            cart = Cart.objects.get(user=user)
            cart_items = CartItem.objects.filter(cart=cart)

            if not cart_items.exists():
                return Response({"detail": "Корзина пуста"}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                total = sum(item.product.price * item.quantity for item in cart_items)

                order = Order.objects.create(user=user, total_price=total)

                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price_per_item=item.product.price
                    )

                cart_items.delete()
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Cart.DoesNotExist:
            return Response({"detail": "Корзина не найдена"}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(tags=["Category"])
class CategoryViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    @extend_schema(
        summary="Получить список категорий товаров",
        responses={200: CategorySerializer(many=True)},
    )
    def list(self, request):
        categories = [{'key': key, 'name': name} for key, name in Product.CATEGORY_CHOICES]
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)