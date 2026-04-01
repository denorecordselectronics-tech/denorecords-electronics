import os
import django
import requests
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bora_electronics.settings')
django.setup()

from products.models import HeroCarousel

# List of professional music/sound system images from Unsplash/Picsum to seed the carousel
# These match the user's requested theme
HERO_IMAGES = [
    {
        "url": "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?q=80&w=2070&auto=format&fit=crop",
        "title": "Professional Sound Systems",
        "subtitle": "Crystal clear audio for concerts, churches, and events.",
        "order": 1
    },
    {
        "url": "https://images.unsplash.com/photo-1514525253361-bee8d4ada807?q=80&w=1924&auto=format&fit=crop",
        "title": "Musical Instruments",
        "subtitle": "From Keyboards to Guitars, find your rhythm today.",
        "order": 2
    },
    {
        "url": "https://images.unsplash.com/photo-1520529618193-27083049580b?q=80&w=2070&auto=format&fit=crop",
        "title": "Home Appliances",
        "subtitle": "Quality fridges, cookers, and more for your home.",
        "order": 3
    },
    {
        "url": "https://images.unsplash.com/photo-1593508512255-86ab42a8e620?q=80&w=1956&auto=format&fit=crop",
        "title": "Visual & TV Systems",
        "subtitle": "Stunning 4K displays and entertainment centers.",
        "order": 4
    }
]

def seed_hero():
    print("Seeding Hero Carousel...")
    # Clear existing items to avoid duplicates during this setup phase
    HeroCarousel.objects.all().delete()
    
    for item in HERO_IMAGES:
        try:
            print(f"  Fetching: {item['title']}...")
            response = requests.get(item['url'], timeout=15)
            if response.status_code == 200:
                filename = f"hero_{item['order']}.jpg"
                carousel_item = HeroCarousel(
                    title=item['title'],
                    subtitle=item['subtitle'],
                    order=item['order'],
                    is_active=True
                )
                carousel_item.image.save(filename, ContentFile(response.content), save=True)
                print(f"    Success: {item['title']} added.")
        except Exception as e:
            print(f"    Error seeding {item['title']}: {e}")

if __name__ == "__main__":
    seed_hero()
