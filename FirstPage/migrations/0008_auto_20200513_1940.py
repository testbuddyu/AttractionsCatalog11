# Generated by Django 3.0.4 on 2020-05-13 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FirstPage', '0007_auto_20200513_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='attractions',
            name='lower_city_name',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='attractions',
            name='lower_name',
            field=models.TextField(default=''),
        ),
    ]
