# Generated by Django 3.2.6 on 2021-09-15 11:19

from django.db import migrations, models
import drf_expiring_token.models


class Migration(migrations.Migration):

    dependencies = [
        ('drf_expiring_token', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expiringtoken',
            name='expires',
            field=models.DateTimeField(default=drf_expiring_token.models.expires_default, verbose_name='Expires in'),
        ),
    ]
