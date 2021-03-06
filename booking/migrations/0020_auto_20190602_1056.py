# Generated by Django 2.2 on 2019-06-02 07:56

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0019_auto_20190530_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='date',
            field=models.DateField(help_text='The date must be future or current but time not passed'),
        ),
        migrations.AlterField(
            model_name='book',
            name='time',
            field=models.TimeField(choices=[(datetime.time(8, 0), '8-9 AM'), (datetime.time(9, 0), '9-10 AM'), (datetime.time(10, 0), '10-11 AM'), (datetime.time(11, 0), '11-12 PM'), (datetime.time(12, 0), '12-1 PM'), (datetime.time(13, 0), '1-2 PM'), (datetime.time(14, 0), '2-3 PM'), (datetime.time(15, 0), '3-4 PM')], help_text='choose a time in the future'),
        ),
        migrations.AlterField(
            model_name='book',
            name='username',
            field=models.ForeignKey(blank=True, help_text='choose a unique username', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='username_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_no',
            field=models.CharField(help_text='must be 10 digits', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='reg_no',
            field=models.CharField(help_text='should be in form of e.g S11/15333/18', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default=None, help_text='must be unique', max_length=20, unique=True),
        ),
    ]
