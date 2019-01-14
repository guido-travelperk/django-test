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

    def Get_All_Recipes_Should_Work(self):
        response = self.client.get(reverse('recipe-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assert_recipe1_is_correct(response.data[0])
        self.assert_recipe2_is_correct(response.data[1])
