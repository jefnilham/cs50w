# Generated by Django 3.2.5 on 2022-08-26 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_comment_comment_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]
