from django.conf import settings
from django.db import models
from cloudinary.models import CloudinaryField


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('fur', 'Меховые изделия'),
        ('coat', 'Шубы'),
        ('jacket', 'Куртки'),
        ('accessory', 'Аксессуары'),
    ]

    name = models.CharField(max_length=255, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name='Категория',
        default='fur'
    )

    description = models.TextField(blank=True, verbose_name='Описание')
    image = CloudinaryField('https://res.cloudinary.com/da74tpgsc/image/upload/v1750327746/images_hqlquy.jpg')
    in_stock = models.BooleanField(default=True, verbose_name='В наличии')
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма заказа', default=0)

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.price_per_item

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'
