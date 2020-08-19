# Generated by Django 3.0.3 on 2020-08-19 08:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0003_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publication',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='book',
            name='uploader',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='book',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(3000), django.core.validators.MinValueValidator(-3000)]),
        ),
    ]
