# Generated by Django 3.2.6 on 2022-10-17 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0007_article_marked_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='feed_link',
            field=models.CharField(default='None', max_length=200),
        ),
    ]
