# Generated by Django 3.0.2 on 2020-01-29 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0009_auto_20200129_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='CheckIn',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='CheckOut',
            field=models.DateField(null=True),
        ),
    ]
