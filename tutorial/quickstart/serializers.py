from rest_framework import serializers

from tutorial.quickstart.models import Recipe, Ingredient


# Ingredients
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'recipe']


# Recipes
class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            Ingredient.objects.create(recipe=recipe, **ingredient)
        return recipe

    def update(self, recipe, validated_data):
        ingredients = validated_data.pop('ingredients')

        recipe.name = validated_data.get('name', recipe.name)
        recipe.description = validated_data.get('description', recipe.description)

        # delete the current ingredients for this recipe form db
        Ingredient.objects.filter(recipe=recipe).delete()

        # add new ingredients to recipe
        for ingredient in ingredients:
            Ingredient.objects.create(recipe=recipe, **ingredient)

        recipe.save()

        return recipe
