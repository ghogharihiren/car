# Generated by Django 3.2.12 on 2022-03-08 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='destination',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='car',
            name='startpoint',
            field=models.CharField(max_length=50),
        ),
    ]