import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoTest.settings')
django.setup()

from app1.models import Product


def create_products():
    products_data = [
        {
            'name': 'Шуба норковая чёрная зимняя Elegance',
            'price': 180000,
            'category': 'coat',
            'description': 'Роскошная норковая шуба до колен, с капюшоном и застёжкой на крючки. Идеальна для холодной зимы.',
            'in_stock': True,
        },
        {
            'name': 'Жилет песцовый серый стильный Luxe',
            'price': 98000,
            'category': 'fur',
            'description': 'Удлинённый меховой жилет из песца, на молнии, безрукавный. Отличный выбор для осенней прогулки.',
            'in_stock': True,
        },
        {
            'name': 'Куртка кожаная бордовая осенняя Classic',
            'price': 45000,
            'category': 'jacket',
            'description': 'Мужская кожаная куртка с подкладкой и молнией. Бордовый цвет придаёт элегантность и стиль.',
            'in_stock': True,
        },
        {
            'name': 'Шапка кашемировая бежевая зимняя',
            'price': 7000,
            'category': 'accessory',
            'description': 'Тёплая и мягкая шапка из кашемира. Идеально сидит по голове и сохраняет тепло в морозы.',
            'in_stock': True,
        },
        {
            'name': 'Шуба чернобурка серая эксклюзивная Royal',
            'price': 210000,
            'category': 'coat',
            'description': 'Премиум шуба из меха чернобурки с поясом. Подходит для торжественных случаев и холодной зимы.',
            'in_stock': False,
        },
        {
            'name': 'Парка джинсовая синяя утеплённая Urban',
            'price': 39000,
            'category': 'jacket',
            'description': 'Молодёжная джинсовая парка с меховой подкладкой. Практична и удобна для городской зимы.',
            'in_stock': True,
        },
        {
            'name': 'Пуховик белый зимний SportStyle',
            'price': 32000,
            'category': 'jacket',
            'description': 'Белый пуховик с капюшоном, лёгкий и очень тёплый. Спортивный стиль с комфортом.',
            'in_stock': True,
        },
        {
            'name': 'Шарф шерстяной бордовый классический',
            'price': 4500,
            'category': 'accessory',
            'description': 'Мужской шерстяной шарф средней длины. Универсален и хорошо сочетается с пальто.',
            'in_stock': True,
        },
        {
            'name': 'Жакет кроличий бежевый элегантный SoftTouch',
            'price': 65000,
            'category': 'fur',
            'description': 'Меховой жакет из натурального кролика. Идеален для офиса и прогулок.',
            'in_stock': True,
        },
        {
            'name': 'Накидка овчинная белая уютная Cozy',
            'price': 74000,
            'category': 'fur',
            'description': 'Женская меховая накидка на плечи из овчины. Мягкая и комфортная.',
            'in_stock': False,
        },
        {
            'name': 'Дублёнка овчинная коричневая теплая Heritage',
            'price': 125000,
            'category': 'coat',
            'description': 'Традиционная дублёнка с меховой отделкой. Отличный выбор на каждый день.',
            'in_stock': True,
        },
        {
            'name': 'Перчатки меховые чёрные женские Chic',
            'price': 6000,
            'category': 'accessory',
            'description': 'Утончённые женские перчатки с мехом внутри. Защищают руки и выглядят элегантно.',
            'in_stock': True,
        },
        {
            'name': 'Жилет енотовый серый городской StylePro',
            'price': 78000,
            'category': 'fur',
            'description': 'Меховой жилет из енота. Универсальный городской стиль для прохладных дней.',
            'in_stock': True,
        },
        {
            'name': 'Пальто замшевое чёрное классическое London',
            'price': 68000,
            'category': 'coat',
            'description': 'Классическое пальто из натуральной замши. Приталенный фасон и скрытая застёжка.',
            'in_stock': True,
        },
        {
            'name': 'Куртка кожаная серая весенняя Milano',
            'price': 47000,
            'category': 'jacket',
            'description': 'Кожаная куртка светло-серого цвета с подкладкой. Подходит для весенних дней.',
            'in_stock': True,
        },
        {
            'name': 'Шапка меховая белая тёплая Arctic',
            'price': 8700,
            'category': 'accessory',
            'description': 'Зимняя меховая шапка с ушками. Сочетается с любой верхней одеждой.',
            'in_stock': True,
        },
        {
            'name': 'Пуховик серый объёмный универсальный',
            'price': 31000,
            'category': 'jacket',
            'description': 'Универсальный пуховик с высоким воротом и капюшоном. Комфорт при -25°C.',
            'in_stock': True,
        },
        {
            'name': 'Жакет овчинный чёрный премиум BlackWolf',
            'price': 92000,
            'category': 'fur',
            'description': 'Стильный жакет из овчины, чёрный цвет, акцент на воротник и талию.',
            'in_stock': False,
        },
        {
            'name': 'Шарф кашемировый серый мужской',
            'price': 5200,
            'category': 'accessory',
            'description': 'Мягкий шарф из кашемира, подходит под классические и повседневные образы.',
            'in_stock': True,
        },
        {
            'name': 'Накидка енотовая рыжая праздничная Foxy',
            'price': 97000,
            'category': 'fur',
            'description': 'Эффектная накидка из меха енота с блеском. Отлична для торжеств.',
            'in_stock': True,
        }
    ]

    Product.objects.all().delete()

    for data in products_data:
        product = Product.objects.create(
            name=data['name'],
            price=data['price'],
            category=data['category'],
            description=data['description'],
            in_stock=data['in_stock'],
            created_at=timezone.now() - timedelta(days=30)
        )
        print(f"✔️ Создан товар: {product.name} — {product.price} руб.")

    print("\n✅ База данных успешно заполнена реальными товарами.")


if __name__ == '__main__':
    create_products()
