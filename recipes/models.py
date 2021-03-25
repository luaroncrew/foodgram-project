from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Following(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='подписчик'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followed_by',
        verbose_name='пользователь'
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'follower'], name='unique following'
            )
        ]

    def __str__(self):
        return (f'Пользователь {self.follower.username}'
                f' подписан на пользователя {self.user.username}')


class Ingredient(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    measurement = models.CharField(
        max_length=10, verbose_name='единица измерения'
    )

    class Meta:
        verbose_name = 'ингредиент и единица измерения'
        verbose_name_plural = 'нигредиенты и единицы измерения'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=15)

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор'
    )
    name = models.CharField(max_length=150, verbose_name='название')
    picture = models.ImageField(
        upload_to='media/', null=True, blank=True, verbose_name='картинка'
    )
    description = models.TextField(
        max_length=1500, blank=True, null=True, verbose_name='описание'
    )
    prep_time = models.PositiveIntegerField(verbose_name='время приготовления')
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='тэги'
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name


class Component(models.Model):
    quantity = models.PositiveIntegerField(verbose_name='количество')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='ingredients'
    )

    class Meta:
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'ингредиенты в рецепте'

    def __str__(self):
        return (f'{self.quantity} '
                f'{self.ingredient.measurement} {self.ingredient}')


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourites',
        verbose_name='пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourites',
        verbose_name='в избранных'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique in favourites'
            )
        ]
        verbose_name = 'избранное'

    def __str__(self):
        return (f'{self.user.username} добавил'
                f' рецепт {self.recipe.name} в избранное')


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='в корзине'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique in wishlist'
            )
        ]
        verbose_name = 'список покупок'

    def __str__(self):
        return (f'{self.user.username} добавил'
                f' рецепт {self.recipe.name} в корзину')
