# Generated by Django 4.2.3 on 2023-07-31 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0027_bidding_new_bid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bidding',
            old_name='user',
            new_name='bid_created_by',
        ),
        migrations.RenameField(
            model_name='bidding',
            old_name='listings',
            new_name='listings_name',
        ),
    ]