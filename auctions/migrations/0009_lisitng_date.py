# Generated by Django 5.1.3 on 2024-12-26 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_lisitng_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='lisitng',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
