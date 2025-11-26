from collections import defaultdict
from utils.strings import is_positive_number

from django.core.exceptions import ValidationError

class RecipeDashboardValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()

    
    def clean(self, *args, **kwargs):
        self.clean_title()
        self.clean_servings()
        self.clean_preparation_time()

        cd = self.data

        title = cd.get('title')
        description = cd.get('description')

    
        if title == description:
            self.errors['title'].append('O titulo não pode ser igual à descrição.')
            self.errors['description'].append('A descrição não pode ser igual ao titulo.')
        
        if self.errors:
            raise self.ErrorClass(self.errors)


    
    def clean_title(self):
        title = self.data.get('title')

        if len(title) < 5:
            self.errors['title'].append('O titulo deve ter ao menos 5 caracteres.')

        return title
    
    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.data.get(field_name)

        if not  is_positive_number(field_value) :
            self.errors[field_name].append('Deve ser um número positivo.')

        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.data.get(field_name)

        if not  is_positive_number(field_value) :
            self.errors[field_name].append('Deve ser um número positivo.')

        return field_value