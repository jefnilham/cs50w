# Generated by Django 3.2.5 on 2022-08-26 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_delete_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_body', models.CharField(max_length=6400)),
                ('comment_datetime', models.DateTimeField(max_length=64)),
                ('comment_username', models.CharField(max_length=64)),
            ],
        ),
    ]
