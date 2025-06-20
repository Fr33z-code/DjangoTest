from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from app1.models import Product


class ProductCatalogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='Fedor', password='1qaz2wsx3edc')
        self.client.login(username='Fedor', password='1qaz2wsx3edc')

        Product.objects.create(
            name="Шуба из норки",
            price=120000,
            category='coat',
            description="Теплая зимняя шуба",
            in_stock=True,
            created_at=timezone.now()
        )

        Product.objects.create(
            name="Аксессуар кожаный",
            price=7000,
            category='accessory',
            description="Модный аксессуар",
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

    def test_search_by_name(self):
        response = self.client.get(reverse('catalog'), {'search': 'аксессуар'})
        self.assertContains(response, "Аксессуар кожаный")
        self.assertNotContains(response, "Шуба из норки")
