# Generated by Django 3.0.4 on 2020-05-06 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FirstPage', '0005_auto_20200426_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='attractions',
            name='photo2',
            field=models.ImageField(default='', upload_to=''),
        ),
        migrations.AddField(
            model_name='attractions',
            name='photo3',
            field=models.ImageField(default='', upload_to=''),
        ),
    ]
