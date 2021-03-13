import csv

from recipes.models import Ingredient


def import_data(filename: str):
    data = open(filename, 'r', encoding='utf-8')
    ingredients_and_measurements = csv.reader(data)

    for item in ingredients_and_measurements:
        ingredient = Ingredient.objects.create(name=item[0], measurement=item[1])
        ingredient.save()
