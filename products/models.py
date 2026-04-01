from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    original_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Used to show strike-through old price")
    image = models.ImageField(upload_to='products/')
    is_available = models.BooleanField(default=True)
    key_features = models.TextField(help_text="Enter features separated by a new line", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def formatted_price(self):
        return f"KES {self.price:,.0f}"

    @property
    def formatted_original_price(self):
        if self.original_price:
            return f"KES {self.original_price:,.0f}"
        return None

    def get_features_list(self):
        return [f.strip() for f in self.key_features.split('\n') if f.strip()]

class HeroCarousel(models.Model):
    image = models.ImageField(upload_to='hero/')
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=500, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Hero Carousel Item"
        verbose_name_plural = "Hero Carousel Items"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title if self.title else f"Carousel Item {self.id}"
