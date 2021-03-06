# Generated by Django 2.2 on 2019-05-15 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_auto_20190510_2152'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('user', models.OneToOneField(default=None, limit_choices_to={'groups__name': 'counsellor'}, on_delete=django.db.models.deletion.CASCADE, related_name='counsellor_profile_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
