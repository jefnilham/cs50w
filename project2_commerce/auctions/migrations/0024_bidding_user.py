# Generated by Django 4.2.3 on 2023-07-31 18:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0023_comment_listings_comment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidding',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
