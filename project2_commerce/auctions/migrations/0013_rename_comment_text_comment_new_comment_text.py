# Generated by Django 4.2.3 on 2023-07-29 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_listing_listing_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment_text',
            new_name='new_comment_text',
        ),
    ]
