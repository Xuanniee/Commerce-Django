# Generated by Django 4.0.5 on 2022-07-15 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_comment_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_listing',
            name='active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]