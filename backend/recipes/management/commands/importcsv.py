import csv
from unicodedata import name
from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load a questions csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
        
    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                Ingredient.objects.create(
                    name=row[0],
                    measurement_unit=row[1]
                )
#https://reddeveloper.ru/questions/kakoi-samyi-prostoi-sposob-importirovat-fail-csv-v-model-django-dyavp?

#python manage.py importcsv --path fixtures/ingredients.csv