# Generated by Django 3.2.6 on 2021-08-30 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210830_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='can_add_posts',
            field=models.BooleanField(default=False),
        ),
    ]