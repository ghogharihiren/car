# Generated by Django 3.2.12 on 2022-03-28 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0022_auto_20220328_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='journy_status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='book',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
