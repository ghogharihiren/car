# Generated by Django 3.2.12 on 2022-04-07 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0027_book_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='status',
        ),
    ]
