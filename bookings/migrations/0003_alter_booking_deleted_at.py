# Generated by Django 3.2.9 on 2021-11-25 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_booking_deleted_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='deleted_at',
            field=models.DateTimeField(null=True),
        ),
    ]
