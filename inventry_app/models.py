import uuid
from django.db import models
from django.utils import timezone

# Create your models here.

#........... supplier..........................
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=15)

    def __str__(self):
        return self.name




#................Items..............................
class Item(models.Model):
    item_code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
#.......................Purchase...........................
class Purchase(models.Model):
    invoice = models.CharField(max_length=10)
    datetime = models.DateField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    total_amount = models.DecimalField(decimal_places=2,max_digits=10)
    
    def __str__(self):
         return self.invoice


class PurchaseDetails(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
   

class Temppurchase(models.Model):
    invoice = models.CharField(max_length=10)
    datetime = models.DateField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    # total_amount = models.DecimalField(decimal_places=2, max_digits=10)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    

#.......................sales..................................
class Sale(models.Model):
    customer = models.CharField(max_length=50)
    contact_no= models.CharField(max_length=11)
    invoice_no = models.CharField( max_length=10)
    datetime = models.DateField(default=timezone.now())
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def generate_invoice_number(self):
        return str(uuid.uuid4().hex[:10])  # Generate a 10-character invoice number, change the length as needed

    def save(self, *args, **kwargs):
        if not self.invoice_no:
            self.invoice_no = self.generate_invoice_number()[:50]

        super(Sale, self).save(*args, **kwargs)


class SaleDetail(models.Model):
    sale =models.ForeignKey(Sale,on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)



class Temsale(models.Model):
    customer = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=11)
    invoice_no = models.CharField(max_length=50) 
    datetime = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
   

    


