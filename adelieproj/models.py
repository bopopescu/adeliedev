from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.utils import timezone

class BillingAddress(models.Model):
    country = models.CharField(max_length=100)
    addressOne = models.CharField(max_length=100)
    addressTwo = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class CreditCard(models.Model):
    name = models.CharField(max_length=200)
    cardNum = models.CharField(max_length=16)
    expirationMonth = models.CharField(max_length=2)
    expirationYear = models.CharField(max_length=4)
    cvc = models.CharField(max_length=5)
    user = models.ForeignKey(User)
    billingAddress = models.ForeignKey(BillingAddress)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ShippingAddress(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    addressOne = models.CharField(max_length=200)
    addressTwo = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def __unicode__(self):
        return self.title
        
class Console(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

class GamePicture(models.Model):
    caption = models.TextField()
    picture = models.ImageField(upload_to='static/pictures/', null=False, blank=False)
    main = models.BooleanField()
    
    def __unicode__(self):
        return self.caption

class GameOrder(models.Model):
    user = models.ForeignKey(User)
    creditCard = models.ForeignKey(CreditCard)
    shippingAddress = models.ForeignKey(ShippingAddress)
    billingAddress = models.ForeignKey(BillingAddress)
    console = models.ForeignKey(Console)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def __unicode__(self):
        return self.user.username

class Game(models.Model):
    title = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    tagLine = models.TextField()
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    shipDate = models.DateField()
    credited = models.BooleanField(default=False)
    pictures = models.ManyToManyField(GamePicture)
    trailerUrl = models.CharField(max_length=100, null=False, default="")
    orders = models.ManyToManyField(GameOrder)
    consoles = models.ManyToManyField(Console)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def __unicode__(self):
        return self.title
        
    def is_active(self):
        return self.startTime <= timezone.now() and self.endTime >= timezone.now()
        
    def is_upcoming(self):
        return self.startTime >= timezone.now()

class GameCredit(models.Model):
    user = models.ForeignKey(User)
    credit = models.FloatField()
    used = models.FloatField(default=0)
    tier = models.IntegerField()
    game = models.ForeignKey(Game)
    gameOrder = models.ForeignKey(GameOrder)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
class CartItem(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    console = models.ForeignKey(Console)
    quantity = models.IntegerField()

class Cart(models.Model):
    user = models.ForeignKey(User)
    checkedOut = models.BooleanField(default=False)
    items = models.ManyToManyField(CartItem)