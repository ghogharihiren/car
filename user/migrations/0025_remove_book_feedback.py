# Generated by Django 3.2.12 on 2022-03-31 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0024_alter_book_bookingseat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='feedback',
        ),
    ]
