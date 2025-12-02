from django.core.exceptions import ValidationError
import pytest
from dashboard.validators import RecipeDashboardValidator

class TestRecipeDashboardValidator:
    def make_data(self, **kwargs):
        data = {
            'title': 'Bolo de Chocolate',
            'description': 'Delicioso bolo',
            'servings': 4,
            'preparation_time': 30,
        }
        data.update(kwargs)
        return data

    def test_valid_data_passes(self):
        data = self.make_data()
        validator = RecipeDashboardValidator(data)
        assert validator.errors == {}

    def test_title_too_short(self):
        data = self.make_data(title='abc')
        with pytest.raises(ValidationError) as exc:
            RecipeDashboardValidator(data)
        assert 'title' in exc.value.message_dict
        assert 'ao menos 5 caracteres' in str(exc.value)

    def test_title_equals_description(self):
        data = self.make_data(title='Igual', description='Igual')
        with pytest.raises(ValidationError) as exc:
            RecipeDashboardValidator(data)
        assert 'title' in exc.value.message_dict
        assert 'description' in exc.value.message_dict
        assert 'não pode ser igual' in str(exc.value)

    def test_negative_servings(self):
        data = self.make_data(servings=-1)
        with pytest.raises(ValidationError) as exc:
            RecipeDashboardValidator(data)
        assert 'servings' in exc.value.message_dict
        assert 'número positivo' in str(exc.value)

    def test_non_number_servings(self):
        data = self.make_data(servings='abc')
        with pytest.raises(ValidationError) as exc:
            RecipeDashboardValidator(data)
        assert 'servings' in exc.value.message_dict
        assert 'número positivo' in str(exc.value)

    def test_negative_preparation_time(self):
        data = self.make_data(preparation_time=-10)
        with pytest.raises(ValidationError) as exc:
            RecipeDashboardValidator(data)
        assert 'preparation_time' in exc.value.message_dict
        assert 'número positivo' in str(exc.value)

    def test_non_number_preparation_time(self):
        data = self.make_data(preparation_time='abc')
        with pytest.raises(ValidationError) as exc:
            RecipeDashboardValidator(data)
        assert 'preparation_time' in exc.value.message_dict
        assert 'número positivo' in str(exc.value)

    def test_multiple_errors(self):
        data = self.make_data(title='a', servings='abc', preparation_time=-1, description='a')
        with pytest.raises(ValidationError) as exc:
            RecipeDashboardValidator(data)
        errors = exc.value.message_dict
        assert 'title' in errors
        assert 'servings' in errors
        assert 'preparation_time' in errors
        assert 'description' in errors
        assert len(errors['title']) >= 1
        assert len(errors['servings']) >= 1
        assert len(errors['preparation_time']) >= 1
        assert len(errors['description']) >= 1