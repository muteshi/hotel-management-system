# Generated by Django 3.0.2 on 2020-03-11 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0009_auto_20200310_2131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartconferenceitems',
            old_name='quantity',
            new_name='conference_duration',
        ),
        migrations.RenameField(
            model_name='cartconferenceitems',
            old_name='stay_duration',
            new_name='guests',
        ),
        migrations.RenameField(
            model_name='cartconferenceitems',
            old_name='line_total',
            new_name='total',
        ),
        migrations.AddField(
            model_name='cartconferenceitems',
            name='RoomCheckIn',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cartconferenceitems',
            name='double_room',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cartconferenceitems',
            name='single_room',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]