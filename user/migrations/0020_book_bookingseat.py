# Generated by Django 3.2.12 on 2022-03-27 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_auto_20220327_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='bookingseat',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
