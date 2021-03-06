# Generated by Django 3.0.2 on 2020-06-08 20:39

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
            name='ConferenceRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_Name', models.CharField(max_length=200)),
                ('room_details', models.TextField(blank=True, null=True)),
                ('room_Capacity', models.PositiveIntegerField(default=10)),
                ('room_Price', models.PositiveIntegerField(default=2000)),
                ('room_discount', models.DecimalField(decimal_places=2, default=1.0, max_digits=1000)),
                ('projector', models.BooleanField(default=False)),
                ('screen', models.BooleanField(default=False)),
                ('conference_phone', models.BooleanField(default=False)),
                ('water', models.BooleanField(default=False)),
                ('free_wifi', models.BooleanField(default=False)),
                ('speakers', models.BooleanField(default=False)),
                ('whiteboard', models.BooleanField(default=False)),
                ('sockets', models.BooleanField(default=False)),
                ('coffee', models.BooleanField(default=False)),
                ('monitors', models.BooleanField(default=False)),
                ('slug', models.SlugField(unique=True)),
                ('published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Conference Rooms',
                'ordering': ('room_Price', 'created_at'),
            },
        ),
        migrations.CreateModel(
            name='Hotels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('property_photo', models.ImageField(default='default.jpg', upload_to='hotel_photos')),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('vat', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('star_rating', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
                ('featured_from', models.DateField(blank=True, null=True)),
                ('featured_to', models.DateField(blank=True, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=12, null=True)),
                ('checkin', models.TimeField(blank=True, null=True)),
                ('checkout', models.TimeField(blank=True, null=True)),
                ('policies', models.TextField(blank=True, null=True)),
                ('has_conference', models.BooleanField(default=False)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('airport_transport', models.BooleanField(default=False)),
                ('night_club', models.BooleanField(default=False)),
                ('wifi', models.BooleanField(default=False)),
                ('parking', models.BooleanField(default=False)),
                ('swimming_pool', models.BooleanField(default=False)),
                ('restaurant', models.BooleanField(default=False)),
                ('gym', models.BooleanField(default=False)),
                ('air_conditioner', models.BooleanField(default=False)),
                ('laundry_services', models.BooleanField(default=False)),
                ('bar_lounge', models.BooleanField(default=False)),
                ('disabled_services', models.BooleanField(default=False)),
                ('elevator', models.BooleanField(default=False)),
                ('shuttle_bus_service', models.BooleanField(default=False)),
                ('cards_accepted', models.BooleanField(default=False)),
                ('contact_person', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Hotels',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='HotelTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Hotel Types',
            },
        ),
        migrations.CreateModel(
            name='PackageTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Package Types',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_photo', models.ImageField(default='default.jpg', upload_to='room_photos')),
                ('room_Name', models.CharField(max_length=200)),
                ('room_details', models.CharField(max_length=500)),
                ('max_adults', models.PositiveIntegerField(default=1)),
                ('max_child', models.PositiveIntegerField(default=1)),
                ('extra_beds', models.PositiveIntegerField(default=0)),
                ('extra_bed_price', models.PositiveIntegerField(default=1)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('room_Price', models.PositiveIntegerField(default=1)),
                ('total_Rooms', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('free_toiletries', models.BooleanField(default=False)),
                ('water_body_view', models.BooleanField(default=False)),
                ('safe_deposit_box', models.BooleanField(default=False)),
                ('lcd_tv', models.BooleanField(default=False)),
                ('pay_tv', models.BooleanField(default=False)),
                ('mini_bar', models.BooleanField(default=False)),
                ('refrigerator', models.BooleanField(default=False)),
                ('blackout_drapes', models.BooleanField(default=False)),
                ('telephone', models.BooleanField(default=False)),
                ('ironing_facilities', models.BooleanField(default=False)),
                ('desk', models.BooleanField(default=False)),
                ('hair_dryer', models.BooleanField(default=False)),
                ('extra_towels', models.BooleanField(default=False)),
                ('bathrobes', models.BooleanField(default=False)),
                ('wake_up_service', models.BooleanField(default=False)),
                ('electric_kettle', models.BooleanField(default=False)),
                ('warddrobe', models.BooleanField(default=False)),
                ('toilet_paper', models.BooleanField(default=False)),
                ('slippers', models.BooleanField(default=False)),
                ('toilet', models.BooleanField(default=False)),
                ('alarm_clock', models.BooleanField(default=False)),
                ('tea_coffee_maker', models.BooleanField(default=False)),
                ('bathtub_shower', models.BooleanField(default=False)),
                ('makeup_shaving_mirror', models.BooleanField(default=False)),
                ('city_view', models.BooleanField(default=False)),
                ('air_conditioner', models.BooleanField(default=False)),
                ('cribs_infant_beds', models.BooleanField(default=False)),
                ('daily_housekeeping', models.BooleanField(default=False)),
                ('garden_view', models.BooleanField(default=False)),
                ('projector', models.BooleanField(default=False)),
                ('screen', models.BooleanField(default=False)),
                ('conference_phone', models.BooleanField(default=False)),
                ('water', models.BooleanField(default=False)),
                ('free_wifi', models.BooleanField(default=False)),
                ('speakers', models.BooleanField(default=False)),
                ('whiteboard', models.BooleanField(default=False)),
                ('sockets', models.BooleanField(default=False)),
                ('coffee', models.BooleanField(default=False)),
                ('monitors', models.BooleanField(default=False)),
                ('hotel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Hotels')),
            ],
            options={
                'verbose_name_plural': 'Rooms',
                'ordering': ['room_Price', 'updated_at'],
            },
        ),
        migrations.CreateModel(
            name='RoomTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Room Types',
            },
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='slider_photos')),
                ('header_text', models.CharField(blank=True, max_length=120, null=True)),
                ('text', models.CharField(blank=True, max_length=120, null=True)),
                ('active', models.BooleanField(default=False)),
                ('featured', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('start_Date', models.DateField(blank=True, null=True)),
                ('end_Date', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Sliders',
                'ordering': ['-start_Date', '-end_Date'],
            },
        ),
        migrations.CreateModel(
            name='RoomPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('image', models.ImageField(upload_to='room_photos')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Room')),
            ],
            options={
                'verbose_name_plural': 'Room Photos',
            },
        ),
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.RoomTypes'),
        ),
        migrations.AddField(
            model_name='room',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('image', models.ImageField(upload_to='hotel_photos')),
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
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('package_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.PackageTypes')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Packages',
                'unique_together': {('title', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='PackagePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('image', models.ImageField(upload_to='package_photos')),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Packages')),
            ],
        ),
        migrations.CreateModel(
            name='Itinirery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
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
        migrations.AddField(
            model_name='hotels',
            name='hotel_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.HotelTypes'),
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
                'ordering': ['package_Price', 'created_at'],
            },
        ),
        migrations.CreateModel(
            name='ConferenceRoomPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('image', models.ImageField(upload_to='room_photos')),
                ('conferenceroom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.ConferenceRoom')),
            ],
            options={
                'verbose_name_plural': 'Conference Room Photos',
            },
        ),
        migrations.AddField(
            model_name='conferenceroom',
            name='hotel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Hotels'),
        ),
        migrations.AddField(
            model_name='conferenceroom',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
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
        migrations.CreateModel(
            name='CartConferenceItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guests', models.PositiveIntegerField(default=1)),
                ('double_room', models.CharField(blank=True, max_length=255, null=True)),
                ('single_room', models.CharField(blank=True, max_length=255, null=True)),
                ('double_room_total', models.PositiveIntegerField(blank=True, null=True)),
                ('single_room_total', models.PositiveIntegerField(blank=True, null=True)),
                ('single_room_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('double_room_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('CheckIn', models.DateField(blank=True, null=True)),
                ('CheckOut', models.DateField(blank=True, null=True)),
                ('RoomCheckIn', models.DateField(blank=True, null=True)),
                ('RoomCheckOut', models.DateField(blank=True, null=True)),
                ('conference_duration', models.PositiveIntegerField(default=1)),
                ('nights', models.PositiveIntegerField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Cart')),
                ('hotel_room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Room')),
                ('rooms', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.ConferenceRoom')),
            ],
            options={
                'verbose_name_plural': 'Conference Cart Items',
            },
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together={('room_Name', 'slug')},
        ),
        migrations.AlterUniqueTogether(
            name='hotels',
            unique_together={('name', 'slug')},
        ),
        migrations.AlterUniqueTogether(
            name='conferenceroom',
            unique_together={('room_Name', 'slug')},
        ),
    ]
