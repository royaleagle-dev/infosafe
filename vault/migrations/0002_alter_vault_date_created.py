# Generated by Django 3.2.8 on 2021-10-24 01:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vault',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
