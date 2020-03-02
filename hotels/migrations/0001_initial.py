# Generated by Django 3.0.2 on 2020-02-27 22:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hotels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('mobile_number', models.CharField(max_length=12)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('property_photo', models.ImageField(default='default.jpg', upload_to='hotel_photos')),
                ('star_rating', models.PositiveIntegerField()),
                ('contact_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Hotels',
                'unique_together': {('name', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_Type', models.CharField(choices=[('Single', 'Single'), ('Double', 'Double'), ('Family', 'Family'), ('Suit', 'Suit')], default='Please Select', max_length=20)),
                ('room_photo', models.ImageField(default='default.jpg', upload_to='room_photos')),
                ('room_Name', models.CharField(max_length=200)),
                ('room_details', models.CharField(max_length=500)),
                ('room_Capacity', models.PositiveIntegerField(default=0)),
                ('slug', models.SlugField(unique=True)),
                ('room_Price', models.PositiveIntegerField(default=0)),
                ('total_Rooms', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hotel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Hotels')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Rooms',
                'unique_together': {('room_Name', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('file', models.ImageField(upload_to='hotel_photos')),
                ('hotel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Hotels')),
            ],
            options={
                'verbose_name_plural': 'Photos',
            },
        ),
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('package_type', models.CharField(choices=[('honeymoon', 'Honeymoon'), ('easter', 'Easter'), ('christmas', 'Christmas'), ('coast', 'Coast'), ('selfdrive', 'Weekend Gateway')], default='honeymoon', max_length=120)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('cover_photo', models.ImageField(default='default.jpg', upload_to='package_photos')),
                ('description', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Packages',
                'unique_together': {('title', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Itinirery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('package_photo', models.ImageField(default='default.jpg', upload_to='itinirery_photos')),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Packages')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Package Itinireries',
            },
        ),
        migrations.CreateModel(
            name='HotelService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('service_photo', models.ImageField(default='default.jpg', upload_to='service_photos')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('hotel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Hotels')),
            ],
            options={
                'verbose_name_plural': 'Services',
            },
        ),
        migrations.CreateModel(
            name='HotelPackages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_Price', models.PositiveIntegerField(default=0)),
                ('meal_Plans', models.TextField()),
                ('duration', models.PositiveIntegerField(default=1)),
                ('start_Date', models.DateField()),
                ('end_Date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hotel', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hotels.Hotels')),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Packages')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Hotel Package',
                'verbose_name_plural': 'Hotel Packages',
            },
        ),
        migrations.CreateModel(
            name='CartPackageItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('line_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('CheckIn', models.DateField(blank=True, null=True)),
                ('CheckOut', models.DateField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Cart')),
                ('hotel_package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.HotelPackages')),
            ],
            options={
                'verbose_name_plural': 'Pakage Cart Items',
            },
        ),
        migrations.CreateModel(
            name='CartItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('line_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('CheckIn', models.DateField(blank=True, null=True)),
                ('CheckOut', models.DateField(blank=True, null=True)),
                ('stay_duration', models.PositiveIntegerField(default=1)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Cart')),
                ('rooms', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Room')),
            ],
            options={
                'verbose_name_plural': 'Cart Items',
            },
        ),
    ]
