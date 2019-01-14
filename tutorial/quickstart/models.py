# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, default='Default description')


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
