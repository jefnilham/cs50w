# Generated by Django 4.2.3 on 2023-07-29 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='listing_description',
            field=models.CharField(default='first description', max_length=1000),
            preserve_default=False,
        ),
    ]