# Generated by Django 4.0.4 on 2022-06-21 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_comment_listing_watchlist_winner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='tempstamp',
            new_name='timestamp',
        ),
    ]
