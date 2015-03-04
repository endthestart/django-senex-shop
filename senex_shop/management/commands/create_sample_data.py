from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = ''
    help = 'Creates data for local development'

    def handle(self, *args, **options):
        # Create a shop
        from senex_shop.core.models import Shop
        shop = Shop(
            name='Senex Shop',
            shop_owner='Shop Owner',
            from_email='info@example.com',
            description='Some description for the shop',
            phone='800.555.1234',
            address_1='1234 Any Street',
            city='Colorado Springs',
            state='CO',
            zip_code='80919'
        )
        shop.save()

        # Create categories
        from senex_shop.models import Category
        bikes, _ = Category.objects.get_or_create(
            name='bikes',
            description='main category for bikes',
            is_active=True,
            ordering=0
        )
        mountain, _ = Category.objects.get_or_create(
            name='mountain',
            description='main category for mountain bikes',
            is_active=True,
            ordering=0,
            parent=bikes
        )
        road, _ = Category.objects.get_or_create(
            name='road',
            description='main category for road bikes',
            is_active=True,
            ordering=0,
            parent=bikes
        )
        accessories, _ = Category.objects.get_or_create(
            name='accessories',
            description='main category for accessories',
            is_active=True,
            ordering=0
        )

        # create products
        from senex_shop.models import Product
        test_bike_1, _ = Product.objects.get_or_create(
            name='Test Bike One',
            category=mountain,
            price=999.95,
            stock=100,
            short_description="Short bicycle description.",
            description="Much longer bicycle description.",
            active=True
        )
        test_bike_2, _ = Product.objects.get_or_create(
            name='Test Bike Two',
            category=road,
            price=999.95,
            stock=100,
            short_description="Short bicycle description.",
            description="Much longer bicycle description.",
            active=True
        )
        test_accessory, _ = Product.objects.get_or_create(
            name='Test Accessory One',
            category=accessories,
            price=999.95,
            stock=100,
            short_description="Short accessory description.",
            description="Much longer accessory description.",
            active=True
        )
        test_bike_1, _ = Product.objects.get_or_create(
            name='Test Accessory Two',
            category=accessories,
            price=999.95,
            stock=100,
            short_description="Short accessory description.",
            description="Much longer accessory description.",
            active=True
        )

        # create option group
        from senex_shop.models import OptionGroup
        option_group, _ = OptionGroup.objects.get_or_create(
            name='size',
            display='Size',
            description='Size option group'
        )

        # create options
        from senex_shop.models import Option
        small_option, _ = Option.objects.get_or_create(
            option_group=option_group,
            name='Small',
            value='s',
            ordering=0
        )
        medium_option, _ = Option.objects.get_or_create(
            option_group=option_group,
            name='Medium',
            value='m',
            ordering=0
        )
        large_option, _ = Option.objects.get_or_create(
            option_group=option_group,
            name='Large',
            value='l',
            ordering=0
        )