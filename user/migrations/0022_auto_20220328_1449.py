# Generated by Django 3.2.12 on 2022-03-28 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_auto_20220327_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='book',
            name='bookingseat',
            field=models.IntegerField(max_length=50),
        ),
    ]
