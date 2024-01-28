# Django
from django.contrib import admin
# Models
from .models import (
    Recipe,
    Product,
    RecipeProduct
)

admin.site.register(Recipe)
admin.site.register(Product)
admin.site.register(RecipeProduct)

