# Generated by Django 3.2.12 on 2022-04-07 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_remove_book_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='status',
        ),
    ]
