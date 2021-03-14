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
    name = models.CharField(max_length=100, verbose_name='название')
    measurement = models.CharField(max_length=10, verbose_name='единица измерения')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    TAGS = [('B', 'ЗАВТРАК'), ('L', 'ОБЕД'), ('D', 'УЖИН')]
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes', verbose_name='автор'
    )
    name = models.CharField(max_length=150, verbose_name='название')
    picture = models.ImageField(null=True, blank=True, verbose_name='картинка')
    description = models.TextField(max_length=1500, blank=True, null=True, verbose_name='описание')
    tag = ArrayField(
        models.CharField(choices=TAGS, max_length=10), null=True, blank=True, verbose_name='тэги'
    )
    prep_time = models.PositiveIntegerField(verbose_name='время приготовления')
    cart = models.ManyToManyField(User, related_name='recipes_in_cart', verbose_name='в корзине')
    favourite = models.ManyToManyField(User, related_name='favourite_recipes', verbose_name='в избранном')

    def __str__(self):
        return self.name


class Component(models.Model):
    qnt = models.IntegerField(verbose_name='количество')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')