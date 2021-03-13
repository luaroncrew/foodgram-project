# Generated by Django 3.0.5 on 2021-03-13 10:07

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0008_auto_20210313_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='qnt',
            field=models.IntegerField(verbose_name='количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cart',
            field=models.ManyToManyField(related_name='recipes_in_cart', to=settings.AUTH_USER_MODEL, verbose_name='в корзине'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='favourite',
            field=models.ManyToManyField(related_name='favourite_recipes', to=settings.AUTH_USER_MODEL, verbose_name='в избранном'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='prep_time',
            field=models.PositiveIntegerField(verbose_name='время приготовления'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tag',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('B', 'ЗАВТРАК'), ('L', 'ОБЕД'), ('D', 'УЖИН')], max_length=10), blank=True, null=True, size=None, verbose_name='тэги'),
        ),
    ]
