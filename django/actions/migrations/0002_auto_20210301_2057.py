# Generated by Django 3.1.7 on 2021-03-01 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='date',
            field=models.DateField(verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='actionsuggestion',
            name='date',
            field=models.DateField(verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='actionsuggestionchanges',
            name='date',
            field=models.DateField(verbose_name='Data'),
        ),
    ]
