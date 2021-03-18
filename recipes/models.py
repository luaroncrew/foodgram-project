from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Following(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        unique_together = ['user', 'follower']

    def __str__(self):
        return f'Пользователь {self.follower.username} подписан на пользователя {self.user.username}'


class Ingredient(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    measurement = models.CharField(max_length=10, verbose_name='единица измерения')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes', verbose_name='автор'
    )
    name = models.CharField(max_length=150, verbose_name='название')
    picture = models.ImageField(upload_to="media/", null=True, blank=True, verbose_name='картинка')
    description = models.TextField(max_length=1500, blank=True, null=True, verbose_name='описание')
    prep_time = models.PositiveIntegerField(verbose_name='время приготовления')
    tags = models.ManyToManyField(Tag, related_name='tags', verbose_name='тэги')

    def __str__(self):
        return self.name


class Component(models.Model):
    qnt = models.IntegerField(verbose_name='количество')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')

    def __str__(self):
        return f'{self.qnt} {self.ingredient.measurement} {self.ingredient}'


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites', verbose_name='пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favourites', verbose_name='в избранных')

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user.username} добавил рецепт {self.recipe.name} в избранное'


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases', verbose_name='пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='purchases', verbose_name='в корзине')

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user.username} добавил рецепт {self.recipe.name} в корзину'
