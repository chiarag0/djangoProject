from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Challenging', 'Challenging'),
    ]

    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'recipes'


class Ingredient(models.Model):
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250)
    quantity = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'recipes'


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    instructions = models.ManyToManyField('Instruction', related_name='recipes', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipes-detail", kwargs={"pk": self.pk})


class Instruction(models.Model):
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE, null=True)
    step = models.TextField()

    def __str__(self):
        return self.step

    class Meta:
        app_label = 'recipes'


# class Tag(models.Model):
#     recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE, null=True)
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         app_label = 'recipes'
