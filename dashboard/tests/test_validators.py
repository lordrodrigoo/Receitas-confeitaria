import pytest
from dashboard.validators import RecipeDashboardValidator
from django.core.exceptions import ValidationError
from collections import defaultdict


def make_data(**kwargs):
    defaults = {
        'title': 'Receita Teste',
        'description': 'Descrição Teste',
        'servings': '2',
        'preparation_time': '10',
    }
    defaults.update(kwargs)
    return defaults

class TestRecipeDashboardValidator:
    def test_valid_data_passes(self):
        data = make_data()
        validator = RecipeDashboardValidator(data)
        assert validator.errors == {}

    @pytest.mark.parametrize('title', ['', 'abc', '1234'])
    def test_title_too_short(self, title):
        data = make_data(title=title)
        with pytest.raises(ValidationError) as exc:
            RecipeDashboardValidator(data)
        assert 'O titulo deve ter ao menos 5 caracteres.' in str(exc.value)

    def test_title_equals_description(self):
        data = make_data(title='igual', description='igual')
        with pytest.raises(ValidationError) as exc:
            RecipeDashboardValidator(data)
        assert 'O titulo não pode ser igual à descrição.' in str(exc.value)
        assert 'A descrição não pode ser igual ao titulo.' in str(exc.value)

    @pytest.mark.parametrize('servings', ['-1', '0', 'abc', None])
    def test_servings_invalid(self, servings):
        data = make_data(servings=servings)
        with pytest.raises(ValidationError) as exc:
            RecipeDashboardValidator(data)
        assert 'Deve ser um número positivo.' in str(exc.value)

    @pytest.mark.parametrize('preparation_time', ['-5', '0', 'xyz', None])
    def test_preparation_time_invalid(self, preparation_time):
        data = make_data(preparation_time=preparation_time)
        with pytest.raises(ValidationError) as exc:
            RecipeDashboardValidator(data)
        assert 'Deve ser um número positivo.' in str(exc.value)

    def test_multiple_errors(self):
        data = make_data(title='a', servings='-1', preparation_time='-2', description='a')
        with pytest.raises(ValidationError) as exc:
            RecipeDashboardValidator(data)
        msg = str(exc.value)
        assert 'O titulo deve ter ao menos 5 caracteres.' in msg
        assert 'Deve ser um número positivo.' in msg
        assert 'O titulo não pode ser igual à descrição.' in msg
        assert 'A descrição não pode ser igual ao titulo.' in msg

    def test_clean_title_returns_title(self):
        data = make_data(title='Título válido')
        validator = RecipeDashboardValidator(data)
        assert validator.clean_title() == 'Título válido'

    def test_clean_title_error(self):
        data = make_data(title='123')
        validator = RecipeDashboardValidator.__new__(RecipeDashboardValidator)
        validator.data = data
        validator.errors = defaultdict(list)
        result = validator.clean_title()
        assert result == '123'
        assert 'O titulo deve ter ao menos 5 caracteres.' in validator.errors['title'][0]

    def test_clean_preparation_time_returns_value(self):
        data = make_data(preparation_time='15')
        validator = RecipeDashboardValidator(data)
        assert validator.clean_preparation_time() == '15'

    def test_clean_preparation_time_error(self):
        data = make_data(preparation_time='-1')
        validator = RecipeDashboardValidator.__new__(RecipeDashboardValidator)
        validator.data = data
        validator.errors = defaultdict(list)
        result = validator.clean_preparation_time()
        assert result == '-1'
        assert 'Deve ser um número positivo.' in validator.errors['preparation_time'][0]

    def test_clean_servings_returns_value(self):
        data = make_data(servings='3')
        validator = RecipeDashboardValidator(data)
        assert validator.clean_servings() == '3'

    def test_clean_servings_error(self):
        data = make_data(servings='-2')
        validator = RecipeDashboardValidator.__new__(RecipeDashboardValidator)
        validator.data = data
        validator.errors = defaultdict(list)
        result = validator.clean_servings()
        assert result == '-2'
        assert 'Deve ser um número positivo.' in validator.errors['servings'][0]

    def test_custom_error_class(self):
        class MyError(Exception): pass
        data = make_data(title='123')
        with pytest.raises(MyError):
            RecipeDashboardValidator(data, ErrorClass=MyError)

    def test_no_errors_does_not_raise(self):
        data = make_data(title='Título válido', description='Outra descrição', servings='2', preparation_time='10')
        validator = RecipeDashboardValidator(data)
        assert validator.errors == {}

    def test_clean_with_no_errors(self):
        data = make_data(title='Título válido', description='Outra descrição', servings='2', preparation_time='10')
        validator = RecipeDashboardValidator.__new__(RecipeDashboardValidator)
        validator.data = data
        validator.errors = {}
        validator.ErrorClass = ValidationError
        validator.clean()
        assert validator.errors == {}
