# Generated by Django 3.0.2 on 2020-03-09 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0004_conferenceroom'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conferenceroom',
            options={'ordering': ('created_at',), 'verbose_name_plural': 'Conference Rooms'},
        ),
        migrations.AlterModelOptions(
            name='hotels',
            options={'ordering': ('created_at',), 'verbose_name_plural': 'Hotels'},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ('created_at',), 'verbose_name_plural': 'Rooms'},
        ),
        migrations.AddField(
            model_name='conferenceroom',
            name='conference',
            field=models.BooleanField(default=False),
        ),
    ]
