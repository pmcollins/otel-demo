# Generated by Django 4.2.2 on 2023-06-30 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desktop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='attributes_hash',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]