# Generated by Django 4.2.3 on 2023-07-31 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0030_remove_bidding_bid_replaced_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='listing_closed',
            field=models.BooleanField(default=False),
        ),
    ]
