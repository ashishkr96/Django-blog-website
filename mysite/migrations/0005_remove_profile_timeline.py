# Generated by Django 2.1.4 on 2019-02-14 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='timeline',
        ),
    ]
