# Generated by Django 4.0.5 on 2022-07-06 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_comment_options_comment_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
