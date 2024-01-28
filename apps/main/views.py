from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from .models import (
    Recipe,
    RecipeProduct,
    Product
)


class MainView(View):
    template_name= 'index.html'
    def get(self,request:HttpRequest)->HttpResponse:
        return render(
            request=request,
            template_name=self.template_name,
            context={}
        )
    
class RecipesView(View):
    template_name = 'recipes.html'
    queryset = Recipe.objects.all()
    def get(self,request:HttpRequest)->HttpResponse:
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'recipes':self.queryset
            }
        )

class MakeRecipeView(View):
    template_name = 'make_recipe.html'
    def get(self,request:HttpRequest)->HttpResponse:
        recipe_name = request.GET.get('recipe_name','')
        if recipe_name:
            try:
                recipe = Recipe.objects.get(title= recipe_name)
            except Recipe.DoesNotExist:
                recipe = Recipe.objects.create(title= recipe_name)
                recipe.save()
                return HttpResponse('Рецепт успешно создан')
            if recipe:
                return HttpResponse('Рецепт с таким названием уже существует')
            

        return render(
            request=request,
            template_name=self.template_name,
            context={}
        )

class RecipeDetailView(View):
    template_name = 'recipe_detail.html'
    recipe_queryset = Recipe.objects.all()
    recipe_product_queryset = RecipeProduct.objects.all()
    def get(self,request:HttpRequest,pk:int)->HttpResponse:
        try:
            recipe = self.recipe_queryset.get(id=pk)
        except Recipe.DoesNotExist:
            return HttpResponse(f'Рецепта с id:{pk} не найдено')
        try:
            details = self.recipe_product_queryset.filter(recipe=recipe)
        except RecipeProduct.DoesNotExist:
            return HttpResponse('Данный рецепт не найден')
        print(request.GET.get('recipe_id'))
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'recipe':details
            }
        )


def add_product_to_recipe_view(request:HttpRequest)->HttpResponse:
    template_name= 'add_product_to_recipe.html'
    recipe_id =request.GET.get('recipe')
    product_id = request.GET.get('product')
    weight = request.GET.get('weight')
    if recipe_id and product_id and weight:
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            product = Product.objects.get(id= product_id)
        except Recipe.DoesNotExist or Product.DoesNotExist:
            return HttpResponse('Такого значения нет в базе данных')
        try:
            rp = RecipeProduct.objects.get(
                recipe=recipe,
                product = product
            )
        except RecipeProduct.DoesNotExist:
            rp = RecipeProduct.objects.create(
                recipe=recipe,
                product = product,
                weight_in_grams = weight
            )
            rp.save()
            return HttpResponse('Вы добавили новый продукт в рецепт')
        rp.weight_in_grams = weight
        rp.save()
        return HttpResponse('Обновлен вес в рецепте')
    recipes = Recipe.objects.all()
    products = Product.objects.all()
    return render(
        request=request,
        template_name=template_name,
        context={
            'recipes':recipes,
            'products':products
        }
    )


def cook_recipe_view(request:HttpRequest):
    recipe_id = request.GET.get('recipe_id')
    if recipe_id:
        try:
            recipe = get_object_or_404(Recipe, id=recipe_id)
        except Recipe.DoesNotExist:
            return HttpResponse(f'Рецепта с id:{recipe_id} не найдено')
        
        recipe_products = RecipeProduct.objects.filter(recipe=recipe)
        for recipe_product in recipe_products:
            recipe_product.product.times_used += 1
            recipe_product.product.save()

        return HttpResponse(f'Блюда по рецепту "{recipe.title}" успешно приготовлены')
    return HttpResponse('Не был передан ID рецепта')


def products_view(request:HttpRequest)->HttpResponse:
    template_name= 'products.html'
    products_qs = Product.objects.all()
    return render(
        request=request,
        template_name=template_name,
        context={
            'products':products_qs
        }
    )


def show_recipes_without_product_view(request:HttpRequest):
    template_name = 'recipes_without_product.html'
    product_id = request.GET.get('product_id')
    if product_id:
        try:
            product = Product.objects.get(id =product_id)
        except Product.DoesNotExist:
            return HttpResponse('Продукта с таким ID нет')
        recipes = Recipe.objects.exclude(
            Q(recipeproduct__product=product) | Q(recipeproduct__product=product, recipeproduct__weight_in_grams__gte=10)
        )
        return render(
            request=request,
            template_name=template_name,
            context={
                'product': product,
                'recipes': recipes
            }
        )
