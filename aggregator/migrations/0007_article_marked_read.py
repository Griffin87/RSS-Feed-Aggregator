# Generated by Django 3.2.6 on 2022-10-13 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0006_alter_source_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='marked_read',
            field=models.BooleanField(default=False),
        ),
    ]
