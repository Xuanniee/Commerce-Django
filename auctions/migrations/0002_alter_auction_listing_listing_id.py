# Generated by Django 4.0.5 on 2022-07-06 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='listing_id',
            field=models.BigAutoField(default=True, primary_key=True, serialize=False),
        ),
    ]
