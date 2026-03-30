import os
import django
import urllib.request
import ssl
from pathlib import Path

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bora_electronics.settings')
django.setup()

# Disable SSL verification for development script
ssl._create_default_https_context = ssl._create_unverified_context

from products.models import Category, Product

def download_image(url, filename):
    media_dir = Path('media/products')
    media_dir.mkdir(parents=True, exist_ok=True)
    filepath = media_dir / filename
    
    print(f"Downloading {filename}...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        return f"products/{filename}"
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return None

def update_catalog():
    # 1. Update/Add Categories
    categories = {
        'home-appliances': Category.objects.get_or_create(name='Home Appliances', slug='home-appliances')[0],
        'music-sound': Category.objects.get_or_create(name='Music & Sound', slug='music-sound')[0],
        'photography': Category.objects.get_or_create(name='Photography', slug='photography')[0],
        'mobile-computing': Category.objects.get_or_create(name='Mobile & Computing', slug='mobile-computing')[0],
    }

    # 2. Product Data Mapping (Unsplash URLs)
    catalog_data = [
        {
            'name': 'Samsung 75-inch Crystal UHD 4K Smart TV',
            'category': categories['home-appliances'],
            'url': 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?q=80&w=2070&auto=format&fit=crop',
            'filename': 'samsung_tv.jpg'
        },
        {
            'name': 'Sony MHC-V73D High Power Audio System',
            'category': categories['music-sound'],
            'url': 'https://images.unsplash.com/photo-1545454675-3531b543be5d?q=80&w=2070&auto=format&fit=crop',
            'filename': 'sony_audio.jpg'
        },
        {
            'name': 'Canon EOS R6 Mark II Mirrorless Camera',
            'category': categories['photography'],
            'url': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?q=80&w=2070&auto=format&fit=crop',
            'filename': 'canon_camera.jpg'
        },
        {
            'name': 'LG Direct Drive Washing Machine 9kg',
            'category': categories['home-appliances'],
            'url': 'https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?q=80&w=2070&auto=format&fit=crop',
            'filename': 'lg_washer.jpg'
        },
        # New Products
        {
            'name': 'Sony HT-S40R 600W 5.1ch Surround Soundbar',
            'category': categories['music-sound'],
            'description': 'Experience real 5.1 channel surround sound with wireless rear speakers and a 3-channel soundbar.',
            'price': 45000,
            'key_features': '600W Total Output\n5.1ch Home Theatre\nWireless Rear Speakers\nBluetooth Connectivity\nHDMI ARC & Optical',
            'url': 'https://images.unsplash.com/photo-1545454675-3531b543be5d?q=80&w=2070&auto=format&fit=crop',
            'filename': 'sony_soundbar.jpg'
        },
        {
            'name': 'JBL PartyBox 110 Portable Party Speaker',
            'category': categories['music-sound'],
            'description': 'Power your party with 160W of powerful sound and built-in LED lights synced to the beat.',
            'price': 38500,
            'key_features': '160W Super High Output\nDynamic Light Show\n12 Hours Playtime\nIPX4 Splashproof\nGuitar & Mic Inputs',
            'url': 'https://images.unsplash.com/photo-1608156639585-34a070dae4c7?q=80&w=2070&auto=format&fit=crop',
            'filename': 'jbl_partybox.jpg'
        },
        {
            'name': 'Apple MacBook Pro 14-inch (M3 Chip)',
            'category': categories['mobile-computing'],
            'description': 'The 14-inch MacBook Pro with M3 is the ultimate pro laptop for everyday creative performance.',
            'price': 245000,
            'key_features': 'Apple M3 Chip\n14.2" Liquid Retina XDR\n8GB Unified Memory\n512GB SSD Storage\nUp to 22 Hours Battery',
            'url': 'https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?q=80&w=2070&auto=format&fit=crop',
            'filename': 'macbook_pro.jpg'
        },
        {
            'name': 'Samsung Galaxy S24 Ultra 512GB',
            'category': categories['mobile-computing'],
            'description': 'Meet Galaxy S24 Ultra, the ultimate form of Galaxy Ultra with a new titanium exterior and 6.8" flat display.',
            'price': 165000,
            'key_features': 'Titanium Frame\n6.8" QHD+ Display\nGalaxy AI Enabled\n200MP Main Camera\nBuilt-in S Pen',
            'url': 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?q=80&w=2070&auto=format&fit=crop',
            'filename': 'samsung_s24.jpg'
        },
        {
            'name': 'Ramtons RM/582 - 20L Solo Microwave',
            'category': categories['home-appliances'],
            'description': 'Simple and reliable 20L solo microwave for everyday heating and defrosting needs.',
            'price': 12500,
            'key_features': '20L Capacity\n700W Power\n5 Power Levels\n95 Minute Timer\nDefrost Function',
            'url': 'https://images.unsplash.com/photo-1574362848149-11496d93a7c7?q=80&w=2070&auto=format&fit=crop',
            'filename': 'ramtons_microwave.jpg'
        },
        {
            'name': 'Mika 270L Low Frost Fridge',
            'category': categories['home-appliances'],
            'description': 'Double door 270L fridge with low frost technology and toughened glass shelves.',
            'price': 58000,
            'key_features': '270L Capacity\nLow Frost Tech\nVC Fresh Filter\nRecessed Handle\nKey and Lock',
            'url': 'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?q=80&w=2070&auto=format&fit=crop',
            'filename': 'mika_fridge.jpg'
        },
        {
            'name': 'Nikon D850 DSLR Camera Body',
            'category': categories['photography'],
            'description': 'Masterful Nikon DSLR with 45.7 megapixels and 4K UHD video recording.',
            'price': 320000,
            'key_features': '45.7 MP Full-Frame\n7 fps Continuous\n4K UHD Video\nWeather Sealed\nTilting Touchscreen',
            'url': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?q=80&w=2070&auto=format&fit=crop',
            'filename': 'nikon_d850.jpg'
        }
    ]

    for item in catalog_data:
        image_path = download_image(item['url'], item['filename'])
        if image_path:
            product, created = Product.objects.update_or_create(
                name=item['name'],
                defaults={
                    'category': item['category'],
                    'image': image_path,
                    'price': item.get('price', 0),
                    'description': item.get('description', 'High-quality electronics from DENO RECORDS ELECTRONICS.'),
                    'key_features': item.get('key_features', ''),
                }
            )
            print(f"{'Created' if created else 'Updated'} product: {product.name}")

if __name__ == '__main__':
    update_catalog()
