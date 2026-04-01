import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bora_electronics.settings')
django.setup()

from products.models import Product, Category

# Make sure we have some categories
music_cat, _ = Category.objects.get_or_create(name="Music & Sound", slug="music-sound")
appliance_cat, _ = Category.objects.get_or_create(name="Home Appliances", slug="home-appliances")
tv_cat, _ = Category.objects.get_or_create(name="TVs & Audio", slug="tvs-audio")
acc_cat, _ = Category.objects.get_or_create(name="Accessories", slug="accessories")

data = [
    ("Yamaha PSR-E583 Keyboard", "60000", "55000", music_cat),
    ("Honda iPower SC4000I-O Generator", "120000", "105000", appliance_cat),
    ("32 Channel Stage Box (50m)", "94000", "85000", music_cat),
    ("M-Audio BX8 D3 Studio Monitor", "52000", "45000", music_cat),
    ("Behringer U-PHORIA Bundle", "21500", "17800", music_cat),
    ("BNK X35B Wireless Microphone", "17800", "15000", music_cat),
    ("M-Audio Oxygen Pro 61", "65000", "60000", music_cat),
    ("UK 3-Pin Power Cable", "800", "500", acc_cat),
    ("Alesis V25 MKII MIDI Controller", "28500", "27000", music_cat),
    ("MXQ-4K 5G Android TV Box", "3450", "3100", tv_cat),
]

for name, orig, sale, cat in data:
    prod, created = Product.objects.get_or_create(
        name=name,
        defaults={
            'original_price': orig,
            'price': sale,
            'category': cat,
            'description': f"High quality {name} available now at Deno Records Electronics"
        }
    )
    if not created:
        prod.original_price = orig
        prod.price = sale
        prod.category = cat
        prod.save()

print("Products populated successfully")
