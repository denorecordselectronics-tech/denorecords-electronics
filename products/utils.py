from django.conf import settings
import urllib.parse

def get_whatsapp_link(product):
    phone = getattr(settings, 'WHATSAPP_PHONE', '2547XXXXXXXX')
    message = f"Hi Deno Records Electronics, I want to buy {product.name} at {product.formatted_price}. Is it available?"
    encoded_message = urllib.parse.quote_plus(message)
    return f"https://wa.me/{phone}?text={encoded_message}"
