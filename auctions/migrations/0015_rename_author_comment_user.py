# Generated by Django 4.0.5 on 2022-07-18 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_rename_user_comment_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='author',
            new_name='user',
        ),
    ]
