from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    qty_total = models.PositiveIntegerField()
    status = models.CharField(
        default='C',
        max_length=1,
        choices = (
            ('A', 'Approved'),
            ('G', 'Generated'),
            ('R', 'Rejected'),
            ('P', 'Pending'),
            ('D', 'Dispatched'),
            ('C', 'Completed'),
        )
    )
    
    def __str__(self):
        return f'Order N. : {self.pk}'
    
class ItemOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    product_id = models.PositiveIntegerField()
    option = models.CharField(max_length=255)
    id_order = models.PositiveIntegerField()
    price = models.FloatField()
    price_promotional = models.FloatField(default=0)
    quantity = models.PositiveIntegerField()
    image = models.CharField(max_length=2000)
    
    def __str__(self):
        return f'Item of {self.order}'