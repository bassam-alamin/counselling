# Generated by Django 2.2 on 2019-06-22 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0022_auto_20190604_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmation',
            name='username',
            field=models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'normal'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usernames', to=settings.AUTH_USER_MODEL),
        ),
    ]
