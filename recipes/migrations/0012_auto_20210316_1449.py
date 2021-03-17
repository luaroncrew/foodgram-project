# Generated by Django 3.0.5 on 2021-03-16 11:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0011_auto_20210316_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cart',
            field=models.ManyToManyField(null=True, related_name='recipes_in_cart', to=settings.AUTH_USER_MODEL, verbose_name='в корзине'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='favourite',
            field=models.ManyToManyField(null=True, related_name='favourite_recipes', to=settings.AUTH_USER_MODEL, verbose_name='в избранном'),
        ),
    ]
