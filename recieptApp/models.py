# Importing necessary modules from Django
from django.db import models
from django.contrib.auth.models import User

# Defining a Django model called Receipt
class Receipt(models.Model):
    # Creating a ForeignKey relationship with the User model. 
    # on_delete=models.SET_NULL: When the referenced User is deleted, set this field to NULL.
    # null=True: Allows this field to be NULL in the database.
    # blank=True: Allows this field to be blank in forms.
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Defining a field for the name of the item on the receipt.
    name = models.CharField(max_length=100, default='something')
    
    # Defining a field for the price of the item.
    price = models.IntegerField(default=0)
    
    # Defining a field for the quantity of the item.
    quantity = models.IntegerField(default=0)
    
    # Defining a field for the total price of the item (price * quantity).
    total = models.IntegerField(default=0)
