# Generated by Django 2.2 on 2019-06-22 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0023_auto_20190622_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmation',
            name='username',
            field=models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'normal.first_name'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usernames', to=settings.AUTH_USER_MODEL),
        ),
    ]
