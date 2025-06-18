import os
import django
from faker import Faker
from django.core.files import File
from io import BytesIO
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoTest.settings')
django.setup()

from app1.models import Product

fake = Faker('ru_RU')


def create_products():
    categories = {
        'coat': ['Шуба', 'Дублёнка', 'Пальто'],
        'fur': ['Жакет', 'Жилет', 'Накидка'],
        'jacket': ['Куртка', 'Пуховик', 'Парка'],
        'accessory': ['Шапка', 'Шарф', 'Перчатки']
    }

    materials = {
        'coat': ['норковая', 'чернобурка', 'песецовая'],
        'fur': ['кроличья', 'овчинная', 'енотовая'],
        'jacket': ['кожаная', 'замшевая', 'джинсовая'],
        'accessory': ['кашемировая', 'шерстяная', 'меховая']
    }

    adjectives = ['элегантная', 'зимняя', 'стильная', 'тёплая', 'эксклюзивная', 'премиум', 'классическая']
    colors = ['чёрная', 'белая', 'коричневая', 'серая', 'бежевая', 'бордовая']

    for i in range(100):
        # Выбираем случайную категорию
        category = random.choice(list(categories.keys()))
        type_product = random.choice(categories[category])
        material = random.choice(materials[category])
        adjective = random.choice(adjectives)
        color = random.choice(colors)

        # Генерируем название
        if category == 'accessory':
            name = f"{type_product} {material} {color}"
        else:
            name = f"{type_product} {material} {color} {adjective}"
            if random.random() > 0.7:
                name += f" {fake.word().capitalize()}"  # Добавляем бренд

        # Генерируем цену
        base_price = random.randint(2000, 5000) * 10
        if category == 'coat':
            price = base_price * 2
        elif category == 'fur':
            price = base_price * 1.5
        else:
            price = base_price

        # Создаем товар
        product = Product.objects.create(
            name=name,
            price=price,
            category=category,
            description=fake.text(max_nb_chars=200),
            in_stock=random.choice([True, True, True, False]),  # 75% chance in stock
            created_at=timezone.now() - timedelta(days=random.randint(0, 365))
        )

        print(f"Создан товар: {name} ({category}) - {price} руб.")


if __name__ == '__main__':
    create_products()
    print("100 тестовых товаров успешно созданы!")
