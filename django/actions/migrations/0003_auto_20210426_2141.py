# Generated by Django 3.1.7 on 2021-04-27 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0002_auto_20210301_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actiontags',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]