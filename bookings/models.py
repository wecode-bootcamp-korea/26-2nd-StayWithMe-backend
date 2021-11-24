from django.db import models

from core.models import TimeStamp

class Booking(TimeStamp):
    user            = models.ForeignKey('users.User', on_delete=models.CASCADE)
    accomodation    = models.ForeignKey('accomodations.Accomodation', on_delete=models.CASCADE)
    room            = models.ForeignKey('accomodations.Room', on_delete=models.CASCADE)
    start_date      = models.DateField()
    end_date        = models.DateField()
    price           = models.DecimalField(max_digits=8, decimal_places=2)
    number_of_adult = models.IntegerField()
    payment_type    = models.ForeignKey('PaymentType', on_delete=models.CASCADE)
    user_request    = models.CharField(max_length=200, null=True)
    name            = models.CharField(max_length=40)
    phone_number    = models.CharField(max_length=15)
    status          = models.ForeignKey('BookingStatus', on_delete=models.CASCADE, default=1)
    deleted_at      = models.DateTimeField(null = True)

    class Meta:
        db_table = 'bookings'

class BookingStatus(TimeStamp):
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'booking_statuses'

class PaymentType(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        db_table = 'payment_types'    
