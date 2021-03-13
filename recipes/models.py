from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

User = get_user_model()


class Following(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_by')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='is_following')

    class Meta:
        unique_together = ['user', 'follower']


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    measurement = models.CharField(max_length=4)


class Component(models.Model):
    qnt = models.IntegerField()
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=150)
    picture = models.ImageField(null=True, blank=True)
    description = models.TextField(max_length=1500, blank=True, null=True)
    ingredients = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    tag = ArrayField(models.CharField(
        max_length=15,
        choices=[(1, 'ЗАВТРАК'), (2, 'ОБЕД'), (3, 'УЖИН')]
    ))
    prep_time = models.PositiveIntegerField()
    cart = models.ManyToManyField(User, related_name='recipes_in_cart')
    favourite = models.ManyToManyField(User, related_name='favourite_recipes')
