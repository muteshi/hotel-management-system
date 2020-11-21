# Generated by Django 3.0.2 on 2020-09-07 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0016_auto_20200907_1444'),
        ('hotels', '0006_hotels_is_apartment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartconferenceitems',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartconferenceitems',
            name='hotel_room',
        ),
        migrations.RemoveField(
            model_name='cartconferenceitems',
            name='rooms',
        ),
        migrations.RemoveField(
            model_name='cartitems',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitems',
            name='rooms',
        ),
        migrations.RemoveField(
            model_name='cartpackageitems',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartpackageitems',
            name='hotel_package',
        ),
        migrations.AlterUniqueTogether(
            name='conferenceroom',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='conferenceroom',
            name='hotel',
        ),
        migrations.RemoveField(
            model_name='conferenceroom',
            name='user',
        ),
        migrations.RemoveField(
            model_name='conferenceroomphoto',
            name='conferenceroom',
        ),
        migrations.RemoveField(
            model_name='hotelservice',
            name='hotel',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartConferenceItems',
        ),
        migrations.DeleteModel(
            name='CartItems',
        ),
        migrations.DeleteModel(
            name='CartPackageItems',
        ),
        migrations.DeleteModel(
            name='ConferenceRoom',
        ),
        migrations.DeleteModel(
            name='ConferenceRoomPhoto',
        ),
        migrations.DeleteModel(
            name='HotelService',
        ),
    ]