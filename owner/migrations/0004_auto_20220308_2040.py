# Generated by Django 3.2.12 on 2022-03-08 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0003_city'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='destination',
            new_name='city',
        ),
        migrations.RemoveField(
            model_name='car',
            name='startpoint',
        ),
    ]
