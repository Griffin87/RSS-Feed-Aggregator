# Generated by Django 3.2.6 on 2022-10-11 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0002_auto_20221011_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='pub_date',
            field=models.DateField(default='1111-11-11'),
        ),
    ]