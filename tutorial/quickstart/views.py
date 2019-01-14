from __future__ import unicode_literals
from rest_framework import viewsets

from tutorial.quickstart.models import Recipe, Ingredient
from tutorial.quickstart.serializers import IngredientSerializer, RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
