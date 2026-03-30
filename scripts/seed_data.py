import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bora_electronics.settings')
django.setup()

from products.models import Category, Product

def seed():
    # Categories
    cats = [
        {'name': 'Home Appliances', 'slug': 'home-appliances'},
        {'name': 'Music & Sound', 'slug': 'music-sound'},
        {'name': 'Photography', 'slug': 'photography'},
    ]
    
    cat_objs = {}
    for cat_data in cats:
        cat, created = Category.objects.get_or_create(**cat_data)
        cat_objs[cat.slug] = cat
        print(f"Category {cat.name} {'created' if created else 'exists'}")

    # Products
    products = [
        {
            'name': 'Samsung 75-inch Crystal UHD 4K Smart TV',
            'category': cat_objs['home-appliances'],
            'description': 'Experience stunningly clear 4K resolution on a massive 75-inch screen. Features Crystal Processor 4K, Smart Hub, and sleek design.',
            'price': 145000,
            'key_features': '75-inch Display\n4K UHD Resolution\nSmart TV Features\nCrystal Processor 4K\n3 HDMI Ports'
        },
        {
            'name': 'Sony MHC-V73D High Power Audio System',
            'category': cat_objs['music-sound'],
            'description': 'Unleash the party with 360° Sound and Light, Jet Bass Booster, and Karaoke features. Perfect for large gatherings and home entertainment.',
            'price': 65000,
            'key_features': '360 Sound & Light\nJet Bass Booster\nGesture Control\nBuilt-in DVD/CD Player\nBluetooth Connectivity'
        },
        {
            'name': 'Canon EOS R6 Mark II Mirrorless Camera',
            'category': cat_objs['photography'],
            'description': 'The Canon EOS R6 Mark II is the most advanced full-frame mirrorless camera in its class, featuring 40 fps electronic shutter and 4K 60p video.',
            'price': 380000,
            'key_features': '24.2 MP Full-Frame Sensor\n4K 60p Internal Video\nUp to 40 fps Shutter\nDual Pixel CMOS AF II\nIn-Body Image Stabilization'
        },
        {
            'name': 'LG Direct Drive Washing Machine 9kg',
            'category': cat_objs['home-appliances'],
            'description': 'Superior cleaning performance with AI Direct Drive technology. Steam function for hygiene and energy efficient.',
            'price': 85000,
            'key_features': '9kg Capacity\nAI Direct Drive\n6 Motion Technology\nSmart Diagnosis\n10 Year Warranty on Motor'
        }
    ]

    for prod_data in products:
        prod, created = Product.objects.get_or_create(
            name=prod_data['name'],
            defaults=prod_data
        )
        print(f"Product {prod.name} {'created' if created else 'exists'}")

if __name__ == '__main__':
    seed()
