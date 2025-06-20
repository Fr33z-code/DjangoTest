from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from app1.models import Product


class ProductCatalogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        Product.objects.create(
            name="Шуба из норки",
            price=120000,
            category='coat',
            description="Теплая зимняя шуба",
            image='https://res.cloudinary.com/da74tpgsc/image/upload/v1750327746/images_hqlquy.jpg',
            in_stock=True,
            created_at=timezone.now()
        )

        Product.objects.create(
            name="Аксессуар кожаный",
            price=7000,
            category='accessory',
            description="Модный аксессуар",
            image='https://res.cloudinary.com/da74tpgsc/image/upload/v1750327746/images_hqlquy.jpg',
            in_stock=False,
            created_at=timezone.now()
        )

    def test_catalog_status_code(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)

    def test_product_names_displayed(self):
        response = self.client.get(reverse('catalog'))
        self.assertContains(response, "Шуба из норки")
        self.assertContains(response, "Аксессуар кожаный")

    def test_filter_by_category(self):
        response = self.client.get(reverse('catalog'), {'category': 'coat'})
        self.assertContains(response, "Шуба из норки")
        self.assertNotContains(response, "Аксессуар кожаный")

    def test_filter_by_in_stock(self):
        response = self.client.get(reverse('catalog'), {'in_stock': 'true'})
        self.assertContains(response, "Шуба из норки")
        self.assertNotContains(response, "Аксессуар кожаный")

    def test_search_by_name(self):
        response = self.client.get(reverse('catalog'), {'search': 'аксессуар'})
        self.assertContains(response, "Аксессуар кожаный")
        self.assertNotContains(response, "Шуба из норки")
