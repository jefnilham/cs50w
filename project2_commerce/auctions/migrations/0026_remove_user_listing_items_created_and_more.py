# Generated by Django 4.2.3 on 2023-07-31 20:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0025_remove_bidding_bid_amount_user_listing_items_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='listing_items_created',
        ),
        migrations.AddField(
            model_name='listing',
            name='listing_created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
