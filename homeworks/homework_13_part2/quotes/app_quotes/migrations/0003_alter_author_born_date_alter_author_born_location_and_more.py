# Generated by Django 5.0.4 on 2024-05-01 19:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_quotes', '0002_alter_author_born_date_alter_author_born_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='born_date',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='author',
            name='born_location',
            field=models.TextField(max_length=64),
        ),
        migrations.AlterField(
            model_name='author',
            name='fullname',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='quote',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_quotes.author'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
