# Generated by Django 4.2.21 on 2025-05-11 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='reviews',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
