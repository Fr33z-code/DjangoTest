import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoTest.settings')
django.setup()

from app1.models import Product

def create_products():
    Product.objects.all().delete()

    categories = {
        'coat': {
            'types': ['Шуба', 'Дублёнка', 'Пальто'],
            'materials': ['норковая', 'чернобурка', 'овчинная'],
        },
        'fur': {
            'types': ['Жакет', 'Жилет', 'Накидка'],
            'materials': ['кроличья', 'енотовая', 'овчинная'],
        },
        'jacket': {
            'types': ['Куртка', 'Пуховик', 'Парка'],
            'materials': ['кожаная', 'джинсовая', 'замшевая'],
        },
        'accessory': {
            'types': ['Шапка', 'Шарф', 'Перчатки'],
            'materials': ['кашемировая', 'шерстяная', 'меховая'],
        },
    }

    adjectives = ['зимняя', 'тёплая', 'элегантная', 'стильная', 'удобная', 'повседневная']
    colors = ['чёрная', 'белая', 'бежевая', 'серая', 'бордовая', 'коричневая']
    brands = ['Elegance', 'RoyalWear', 'UrbanStyle', 'SoftTouch', 'ChicLine', 'FrostyFox']

    short_descriptions = {
        'coat': "Тёплая верхняя одежда из {material} меха.",
        'fur': "Лёгкий меховой вариант на прохладную погоду.",
        'jacket': "Практичная модель для города.",
        'accessory': "Аксессуар для защиты от холода.",
    }

    index = 1

    for _ in range(100):
        category = list(categories.keys())[(index - 1) % 4]
        data = categories[category]

        type_name = data['types'][index % len(data['types'])]
        material = data['materials'][index % len(data['materials'])]
        adjective = adjectives[index % len(adjectives)]
        color = colors[index % len(colors)]
        brand = brands[index % len(brands)]

        name_parts = [type_name, material, color, adjective]
        if category != 'accessory':
            name_parts.append(brand)
        name = " ".join(name_parts)

        base_price = 5000 + index * 500
        if category == 'coat':
            price = base_price * 2
        elif category == 'fur':
            price = base_price * 1.5
        else:
            price = base_price

        description = short_descriptions[category].format(material=material.capitalize())

        Product.objects.create(
            name=name,
            price=int(price),
            category=category,
            description=description,
            in_stock=True if index % 7 != 0 else False,
            created_at=timezone.now() - timedelta(days=index)
        )

        print(f"✅ {index}: {name} — {int(price)} руб.")
        index += 1

    print("\n🎉 100 товаров успешно созданы!")

if __name__ == '__main__':
    create_products()
