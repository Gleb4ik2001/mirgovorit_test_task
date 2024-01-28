from django.db import models

class Product(models.Model):
    title = models.CharField(
        verbose_name = 'название продукта',
        max_length = 150,
        unique = True
    )
    times_used=  models.IntegerField(
        verbose_name = 'количество использований в рецептах',
        default = 0
    )

    def __str__(self) -> str:
        return f"{self.title} | {self.times_used}"
    
    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('-id',)

class Recipe(models.Model):
    title = models.CharField(
        verbose_name = 'название рецепта',
        max_length =100
    )
    products = models.ManyToManyField(
        verbose_name='продукты',
        to=Product,
        through='RecipeProduct'
    )

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural ='рецепты'
        ordering = ('-id',)

class RecipeProduct(models.Model):
    recipe = models.ForeignKey(
        verbose_name = 'рецепт',
        to = Recipe,
        on_delete = models.CASCADE
    )
    product = models.ForeignKey(
        verbose_name = 'продукт',
        to=Product,
        on_delete = models.CASCADE,
    )
    weight_in_grams = models.DecimalField(
    verbose_name='вес в граммах',
    max_digits=10,
    decimal_places=2,
    )

    def __str__(self) -> str:
        return f'{self.recipe.title} | {self.product.title}'
    
    class Meta:
        verbose_name ='рецепт/продукт'
        verbose_name_plural = 'рецепты/продукты'
        ordering = ('-id',)
        unique_together = ('recipe', 'product')
