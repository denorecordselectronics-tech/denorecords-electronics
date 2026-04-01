import os
import io
import urllib.request
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Product, Category, HeroCarousel
import requests


# Product data: (name, original_price, sale_price, category_slug, category_name, description, features, image_query)
PRODUCTS = [
    (
        "Yamaha PSR-E583 Keyboard",
        60000, 55000,
        "music-sound", "Music & Sound",
        "The Yamaha PSR-E583 is a feature-packed 61-key portable keyboard perfect for beginners and intermediate players. With over 800 instrument voices, 290 auto accompaniment styles, and built-in lessons, it's the ideal learning companion.",
        "61 Touch-sensitive Keys\n800+ Instrument Voices\n290 Auto Accompaniment Styles\nBluetooth Audio & MIDI\nUSB to Host connectivity\nBuilt-in Microphone Input",
        "yamaha+keyboard+PSR",
    ),
    (
        "Honda iPower SC4000I-O Generator",
        120000, 105000,
        "home-appliances", "Home Appliances",
        "The Honda iPower SC4000I-O is a super quiet, inverter generator ideal for home backup power, outdoor events, and professional use. Featuring advanced Eco-Throttle technology for maximum fuel efficiency.",
        "4000W Maximum Output\nSuper Quiet Inverter Technology\nEco-Throttle for Fuel Efficiency\nParallel Operation Capable\nElectric Start\n3 Year Manufacturer Warranty",
        "honda+generator+inverter",
    ),
    (
        "32 Channel Stage Box (50m)",
        94000, 85000,
        "music-sound", "Music & Sound",
        "Professional 32-channel stage box with 50M multicore cable for live sound applications. Ideal for large concerts, theatres, and venues requiring reliable, high-quality audio signal transport.",
        "32 Input Channels\n50 Meter Multicore Cable\nXLR Male & Female Connectors\nHeavy Duty Steel Construction\nColor-coded channels\nLow noise signal path",
        "stage+box+audio+multicore",
    ),
    (
        "M-Audio BX8 D3 Studio Monitor",
        52000, 45000,
        "music-sound", "Music & Sound",
        "The M-Audio BX8 D3 is a professional 8-inch studio monitor designed for accurate, high-definition sound reproduction in recording studios and home studios.",
        "8-inch Low-Frequency Driver\n1.5-inch Silk Dome Tweeter\n150W Bi-Amplified\nXLR & TRS Inputs\nAcoustic Space Control\nHigh-pass filter for versatility",
        "studio+monitor+speaker",
    ),
    (
        "Behringer U-PHORIA Bundle",
        21500, 17800,
        "music-sound", "Music & Sound",
        "The Behringer U-PHORIA Bundle is the complete starter package for home recording. Includes USB audio interface, condenser microphone, headphones, and all necessary cables.",
        "USB Audio Interface Included\nCondenser Microphone\nMonitoring Headphones\nXLR-TRS Cables Included\nPlug & Play USB\nCompatible with All DAWs",
        "behringer+audio+interface+bundle",
    ),
    (
        "BNK X35B Wireless Microphone",
        17800, 15000,
        "music-sound", "Music & Sound",
        "The BNK X35B UHF Wireless Microphone System delivers professional-quality wireless audio for live performances, presentations, and events. Features both handheld and lapel microphone options.",
        "UHF Wireless Technology\nUp to 80m Operating Range\nHandheld + Lapel Microphone\nLCD Display on Receiver\nRechargeable Battery\nAnti-interference Technology",
        "wireless+microphone+UHF",
    ),
    (
        "M-Audio Oxygen Pro 61",
        65000, 60000,
        "music-sound", "Music & Sound",
        "The M-Audio Oxygen Pro 61 is a 61-key premium USB MIDI keyboard controller with professional features including velocity-sensitive keys, 16 RGB pads, and deep DAW integration.",
        "61 Semi-Weighted Keys\n16 RGB Backlit Performance Pads\n9 Assignable Faders\n8 Endless Encoders\nAuto-Mapping for major DAWs\nUSB Bus Powered",
        "MIDI+keyboard+controller+61+key",
    ),
    (
        "UK 3-Pin Power Cable",
        800, 500,
        "accessories", "Accessories",
        "Heavy duty UK 3-Pin standard IEC power cable compatible with computers, monitors, audio equipment, and most home appliances. 1.8 metres long with thick, durable insulation.",
        "UK 3-Pin Standard Plug\n1.8 Metre Length\nHeavy Duty Insulation\nIEC C13 Connector\n10A / 250V Rated\nUniversal Compatibility",
        "power+cable+UK+plug",
    ),
    (
        "Alesis V25 MKII MIDI Controller",
        28500, 27000,
        "music-sound", "Music & Sound",
        "The Alesis V25 MKII is a compact 25-key USB MIDI keyboard controller ideal for producers and beatmakers on the go. Features velocity-sensitive pads and deep software integration.",
        "25 Full-Size Keys\n8 Backlit Velocity-Sensitive Pads\n4 Assignable Knobs\nUSB Bus Powered\nPlug & Play\nCompatible with all major DAWs",
        "alesis+midi+keyboard+controller",
    ),
    (
        "MXQ-4K 5G Android TV Box",
        3450, 3100,
        "tvs-audio", "TVs & Audio",
        "Transform any TV into a smart TV with the MXQ-4K 5G Android TV Box. Stream Netflix, YouTube, and thousands of apps in stunning 4K Ultra HD. Dual-band WiFi for fast, stable streaming.",
        "4K Ultra HD Streaming\nAndroid OS\nDual-Band 5G WiFi\n1GB RAM / 8GB Storage\nHDMI Output\nRemote Control Included",
        "android+TV+box+4K",
    ),
]

HERO_IMAGES = [
    {
        "url": "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?q=80&w=2070&auto=format&fit=crop",
        "title": "Professional Sound Systems",
        "subtitle": "Concert-ready speakers, amplifiers & PA systems. Trusted by DJs and event organizers across Kenya.",
        "order": 1
    },
    {
        "url": "https://images.unsplash.com/photo-1514525253361-bee8d4ada807?q=80&w=1924&auto=format&fit=crop",
        "title": "Studio & Recording Gear",
        "subtitle": "From microphones to MIDI controllers — everything you need to produce, record, and perform.",
        "order": 2
    },
    {
        "url": "https://images.unsplash.com/photo-1520529618193-27083049580b?q=80&w=2070&auto=format&fit=crop",
        "title": "Musical Instruments",
        "subtitle": "Keyboards, guitars, and more. Quality instruments for beginners and professionals alike.",
        "order": 3
    },
    {
        "url": "https://images.unsplash.com/photo-1593508512255-86ab42a8e620?q=80&w=1956&auto=format&fit=crop",
        "title": "Live Event Equipment",
        "subtitle": "Mixers, stage boxes, and wireless microphones. Power your next event with pro-grade gear.",
        "order": 4
    },
    {
        "url": "https://images.unsplash.com/photo-1550009158-9ebf69173e03?q=80&w=2001&auto=format&fit=crop",
        "title": "Home Entertainment",
        "subtitle": "Smart TV boxes, cameras, and home appliances delivered to your doorstep nationwide.",
        "order": 5
    }
]


def fetch_placeholder_image(query, index):
    """Fetch a placeholder image from Picsum (reliable, no auth needed)."""
    # Use picsum.photos – random but seeded image per product index
    seed = 100 + index
    url = f"https://picsum.photos/seed/{seed}/600/600"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read()
    except Exception as e:
        print(f"  Warning: Could not fetch image for {query}: {e}")
        return None


class Command(BaseCommand):
    help = "Populates the database with sample products and placeholder images."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting product population..."))

        for i, (name, orig_price, sale_price, cat_slug, cat_name, desc, features, img_query) in enumerate(PRODUCTS):
            # Ensure category exists
            category, _ = Category.objects.get_or_create(
                slug=cat_slug,
                defaults={'name': cat_name}
            )

            # Create or update product
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'original_price': orig_price,
                    'price': sale_price,
                    'description': desc,
                    'key_features': features,
                    'is_available': True,
                }
            )
            if not created:
                product.original_price = orig_price
                product.price = sale_price
                product.description = desc
                product.key_features = features
                product.category = category
                product.is_available = True

            # Fetch and attach placeholder image if no image set
            if not product.image:
                self.stdout.write(f"  Fetching placeholder image for: {name}")
                img_data = fetch_placeholder_image(img_query, i)
                if img_data:
                    filename = f"product_{cat_slug}_{i+1}.jpg"
                    product.image.save(filename, ContentFile(img_data), save=False)

            product.save()
            status = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"  [{status}] {name} — KES {sale_price:,} (was KES {orig_price:,})"))

        self.stdout.write(self.style.SUCCESS("\nProducts populated successfully!"))

        self.stdout.write(self.style.NOTICE("Starting Hero Carousel population..."))
        # Clear existing items to avoid duplicates
        HeroCarousel.objects.all().delete()

        for item in HERO_IMAGES:
            try:
                self.stdout.write(f"  Fetching: {item['title']}...")
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
                    self.stdout.write(self.style.SUCCESS(f"    Success: {item['title']} added."))
                else:
                    self.stdout.write(self.style.ERROR(f"    Failed to fetch {item['title']}: Status {response.status_code}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"    Error seeding {item['title']}: {e}"))
                
        self.stdout.write(self.style.SUCCESS("\nAll tasks completed successfully!"))
