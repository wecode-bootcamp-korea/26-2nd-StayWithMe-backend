from django.db import models
from django.db.models.base import Model

from core.models import TimeStamp

class Category(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        db_table = 'categories'

class Accomodation(TimeStamp):
    name         = models.CharField(max_length=40)
    introduction = models.CharField(max_length=200)
    address      = models.CharField(max_length=100)
    longitude    = models.DecimalField(max_digits=13, decimal_places=10,default=0.0)
    latitude     = models.DecimalField(max_digits=13, decimal_places=10,default=0.0)
    phone_number = models.CharField(max_length=40)
    email        = models.CharField(max_length=40)
    category     = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'accomodations'
    
class AccomodationImage(models.Model):
    image_url          = models.CharField(max_length=2000)
    accomodation = models.ForeignKey('Accomodation', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'accomodation_images'

class Room(TimeStamp):
    name          = models.CharField(max_length=40)
    max_people    = models.IntegerField()
    min_people    = models.IntegerField()
    price         = models.DecimalField(max_digits=10, decimal_places=2)
    accomodation  = models.ForeignKey('Accomodation', on_delete=models.CASCADE)
    number_of_bed = models.IntegerField()
    option        = models.ManyToManyField('Option', through='RoomOption', related_name='rooms')

    class Meta:
        db_table = 'rooms'

class RoomImage(models.Model):
    room      = models.ForeignKey('Room', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=2000)

    class Meta:
        db_table = 'room_images'
    
class Option(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        db_table = 'options'

class RoomOption(models.Model):
    room   = models.ForeignKey('Room', on_delete=models.CASCADE)
    option = models.ForeignKey('Option', on_delete=models.CASCADE)

    class Meta:
        db_table = 'room_options'