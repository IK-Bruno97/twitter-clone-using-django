# Generated by Django 4.1.2 on 2023-01-24 13:15

from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200422_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='favorite_color',
            field=users.models.RGBcolorField(max_length=6, null=True),
        ),
    ]
