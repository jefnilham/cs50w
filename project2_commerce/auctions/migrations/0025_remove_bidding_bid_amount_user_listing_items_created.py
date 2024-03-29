# Generated by Django 4.2.3 on 2023-07-31 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0024_bidding_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bidding',
            name='bid_amount',
        ),
        migrations.AddField(
            model_name='user',
            name='listing_items_created',
            field=models.ManyToManyField(related_name='listing_items_created', to='auctions.listing'),
        ),
    ]
