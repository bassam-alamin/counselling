# Generated by Django 2.2 on 2019-05-10 21:52

import booking.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_auto_20190507_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='date',
            field=models.DateField(validators=[booking.validators.validate_date]),
        ),
    ]
