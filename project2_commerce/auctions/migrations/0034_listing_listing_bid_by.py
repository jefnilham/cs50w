# Generated by Django 4.2.3 on 2023-07-31 22:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0033_remove_user_listing_closed_listing_listing_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='listing_bid_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winning_bidder', to=settings.AUTH_USER_MODEL),
        ),
    ]
