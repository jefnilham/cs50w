# Generated by Django 4.2.3 on 2023-07-30 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_rename_watchlist_listings_watchlist_listings_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='listings',
            new_name='possible_listings_to_add',
        ),
    ]
