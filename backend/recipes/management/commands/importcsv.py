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
            #reader = csv.reader(f, dialect='excel')
            reader = csv.reader(f, delimiter=',')
            
            for row in reader:
                Ingredient.objects.create(
                    name=row[0],
                    
                    measurement_unit=row[1]
                )
# Если вы сохранили его как app/management/commands/load_questions.py, вы бы вызывали его как:

# python manage.py load_questions --path /path/to/your/file.csv
#https://reddeveloper.ru/questions/kakoi-samyi-prostoi-sposob-importirovat-fail-csv-v-model-django-dyavp?
#C:\Dev\foodgram-project-react\backend\management\commands\importcsv.py