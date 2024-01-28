from django.urls import path
from .views import (
    MainView,
    RecipesView,
    MakeRecipeView,
    RecipeDetailView,
    add_product_to_recipe_view,
    cook_recipe_view,
    products_view,
    show_recipes_without_product_view
)


urlpatterns = [
    path('', MainView.as_view(),name='main_view'),
    path('recipes/',RecipesView.as_view(),name='recipes_view'),
    path('make_recipe/',MakeRecipeView.as_view(),name='make_recipe'),
    path('recipe_detail/<int:pk>/',RecipeDetailView.as_view(),name='recipe_detail'),
    path('add_product_to_recipe/',add_product_to_recipe_view,name='add_product_to_recipe'),
    path('cook_recipe/',cook_recipe_view,name='cook_recipe'),
    path('products/',products_view,name='products'),
    path('recipes_without_product/',show_recipes_without_product_view,name='show_recipes_without_product')
]
