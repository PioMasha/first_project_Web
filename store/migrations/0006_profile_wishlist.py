# Generated by Django 4.2 on 2024-02-11 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='wishlist',
            field=models.ManyToManyField(blank=True, related_name='wishlisted_by', to='store.product'),
        ),
    ]
