# Generated by Django 3.0.4 on 2020-04-23 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FirstPage', '0002_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attractions',
            name='photo',
            field=models.ImageField(default='', upload_to='media/'),
        ),
    ]