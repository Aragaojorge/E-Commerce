from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField(max_length=255)
    long_description = models.TextField()
    image = models.ImageField(upload_to='product_images/%Y/%m/', blank=True, null=True)
    slug = models.SlugField(unique=True)
    price_marketing = models.FloatField()
    price_marketing_promotional = models.FloatField(default=0)
    type = models.CharField(default='V', max_length=1, choices=(('O', 'Option'), ('S', 'Simple'),))
    
    @staticmethod
    def resize_image(img, new_width=800):
        print(img.name)
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        max_image_size = 800
        
        if self.image:
            self.resize_image(self.image, max_image_size)
    
    def __str__(self):
        return self.name