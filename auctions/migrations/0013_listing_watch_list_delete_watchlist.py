# Generated by Django 5.1.3 on 2024-12-26 21:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_remove_listing_watchlist_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watch_list',
            field=models.ManyToManyField(blank=True, related_name='watch_lists', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='WatchList',
        ),
    ]
