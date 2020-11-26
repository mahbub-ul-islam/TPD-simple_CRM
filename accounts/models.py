from django.db import models

# Create your models here.


class Customer(models.Model):

    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.name


class Product(models.Model):

    CATAGORY = (
                    ('Indoor', 'Indoor'),
                    ('Out Door', 'Out Door'),
                )

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    catagory = models.CharField(max_length=100, null=True, choices=CATAGORY)
    description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)



class Order(models.Model):

    STATUS = (
                ('Pending', 'Pending'),
                ('Out of delivery', 'Out of delivery'),
                ('Delivered', 'Delivered'),
            )

    #customer = 
    #product = 
    status = models.CharField(max_length=100, null=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, null=True)