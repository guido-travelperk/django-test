# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tutorial.quickstart.models import Recipe, Ingredient


class RecipesTests(APITestCase):

    def setUp(self):
        recipe1 = Recipe.objects.create(name='TestName1', description="TestDescription1")
        Recipe.objects.create(name='TestName2', description="TestDescription2")

        Ingredient.objects.create(recipe=recipe1, name='TestIngredient 1')
        Ingredient.objects.create(recipe=recipe1, name='TestIngredient 2')

    def assert_recipe1_is_correct(self, recipe_data):
        self.assertEqual(recipe_data['name'], 'TestName1')
        self.assertEqual(recipe_data['description'], 'TestDescription1')
        self.assertEqual(len(recipe_data['ingredients']), 2)
        self.assertEqual(recipe_data['ingredients'][0]['name'], 'TestIngredient 1')
        self.assertEqual(recipe_data['ingredients'][1]['name'], 'TestIngredient 2')

    def assert_recipe2_is_correct(self, recipe_data):
        self.assertEqual(recipe_data['name'], 'TestName2')
        self.assertEqual(recipe_data['description'], 'TestDescription2')
        self.assertEqual(len(recipe_data['ingredients']), 0)

    def test_get_all_recipes_should_work(self):
        # Act
        response = self.client.get(reverse('recipe-list'))

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assert_recipe1_is_correct(response.data[0])
        self.assert_recipe2_is_correct(response.data[1])

    def test_get_recipe_detail_should_work(self):
        # Arrange
        recipe = Recipe.objects.filter(name='TestName1').get()

        # Act
        response = self.client.get(reverse('recipe-detail', args=[recipe.id]))

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_recipe1_is_correct(response.data)

    def test_update_recipe_should_work(self):
        # Arrange
        recipe = Recipe.objects.filter(name='TestName1').get()
        data = {'name': 'ChangedName', 'description': 'ChangedDescription',
                'ingredients': [{'name': 'ChangedIngredient'}]}

        # Act
        response = self.client.put(reverse('recipe-detail', args=[recipe.id]), data, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_recipe = Recipe.objects.filter(name='ChangedName').get()

        self.assertEqual(updated_recipe.description, 'ChangedDescription')
        ingredients = updated_recipe.ingredients.all()
        self.assertEqual(len(ingredients), 1)
        self.assertEqual(ingredients[0].name, 'ChangedIngredient')

    def test_delete_recipe_should_work(self):
        # Arrange
        recipe = Recipe.objects.filter(name='TestName1').get()

        # Act
        response = self.client.delete(reverse('recipe-detail', args=[recipe.id]))

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        result = Recipe.objects.filter(name='TestName1')

        self.assertEqual(result.count(), 0)

    def test_create_recipe_should_work(self):
        # Arrange
        data = {'name': 'NewName', 'description': 'NewDescription',
                'ingredients': [{'name': 'NewIngredient1'}, {'name': 'NewIngredient2'}]}

        # Act
        response = self.client.post(reverse('recipe-list'), data, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.filter(name='NewName').get()

        self.assertEqual(recipe.description, 'NewDescription')
        ingredients = recipe.ingredients.all()
        self.assertEqual(len(ingredients), 2)
        self.assertEqual(ingredients[0].name, 'NewIngredient1')
        self.assertEqual(ingredients[1].name, 'NewIngredient2')
