from django.db import models
import uuid
from django.utils import timezone


class Login(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )
    email = models.CharField(max_length=100, blank=False, null=False)
    password = models.CharField(max_length=100, blank=False, null=False)
    phonenumber = models.CharField(max_length=15, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=18, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)


class Items(models.Model):
    item = models.CharField(max_length=100, blank=True, null=True)
    rate = models.CharField(max_length=18, blank=True, null=True)

class Hotels(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )
    restaurantName = models.CharField(max_length=100, blank=False, null=False)
    rating = models.CharField(max_length=100, blank=False, null=False)
    deliveryTime = models.CharField(max_length=15, blank=True,null=False)
    items = models.ManyToManyField(Items, related_name='hotels')
    cityLocation = models.CharField(max_length=100, blank=True, null=True)
    distance = models.CharField(max_length=18, blank=True, null=True)
    city = models.CharField(max_length=18, blank=True, null=True)

class Cart(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )
    userId = models.UUIDField()
    item = models.CharField(max_length=100, blank=True, null=True)
    HotelName = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    Hotellocation = models.CharField(max_length=100, blank=True, null=True)
    itemRate = models.IntegerField(blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    deliveryTime = models.IntegerField(blank=True, null=True)

class ItemsOrdered(models.Model):
    item = models.CharField(max_length=200, blank=True, null=True)
    itemCount = models.CharField(max_length=100, blank=True, null=True)
    rate = models.CharField(max_length=18, blank=True, null=True)

class OrderData(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )
    userId = models.UUIDField()
    HotelName = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    Hotellocation = models.CharField(max_length=100, blank=True, null=True)
    item = models.ManyToManyField(ItemsOrdered, related_name='OrderedItems')
    totalItems = models.IntegerField(blank=True, null=True)
    deliveryTime = models.IntegerField(blank=True, null=True)
    deliveryPerson = models.CharField(max_length=100, blank=True, null=True)
    TotalItemAmount = models.IntegerField(blank=True, null=True)
    TotalPay = models.IntegerField(blank=True, null=True)
    orderStatus = models.CharField(max_length=100, blank=True, null=True)
    orderTime = models.DateTimeField(default=timezone.now)




