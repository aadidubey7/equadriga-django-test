from django.db import models
from django.db.models import Sum

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    @classmethod
    def get_item_by_name(self, item_name):
        return Item.objects.filter(name=item_name)
    
    @classmethod
    def get_total_price(self):
        return Item.objects.aggregate(total=Sum('price'))['total']