import pytest
from django.core.exceptions import ValidationError
from utils import strings, pagination, django_forms, environment

# --- utils/strings.py ---
def test_is_positive_number():
    assert strings.is_positive_number(5)
    assert strings.is_positive_number('10')
    assert not strings.is_positive_number(-1)
    assert not strings.is_positive_number('abc')
    assert not strings.is_positive_number(None)
    assert not strings.is_positive_number('')

# --- utils/pagination.py ---
def test_make_pagination_range_basic():
    page_range = list(range(1, 11))
    result = pagination.make_pagination_range(page_range, 4, 5)
    assert 'pagination' in result
    assert result['current_page'] == 5
    assert isinstance(result['pagination'], list)
    assert all(p in page_range for p in result['pagination'])

def test_make_pagination_handles_small_range():
    page_range = [1, 2, 3]
    result = pagination.make_pagination_range(page_range, 2, 1)
    assert result['pagination'] == [1, 2, 3][:result['stop_range']]

# --- utils/django_forms.py ---
def test_add_attr_and_placeholder():
    class DummyWidget:
        def __init__(self):
            self.attrs = {}
    class DummyField:
        def __init__(self):
            self.widget = DummyWidget()
    field = DummyField()
    django_forms.add_attr(field, 'class', 'my-class')
    assert field.widget.attrs['class'] == 'my-class'
    django_forms.add_placeholder(field, 'Digite aqui')
    assert field.widget.attrs['placeholder'] == 'Digite aqui'

def test_strong_password_valid():
    django_forms.strong_password('Abcdefg1')  # Should not raise

def test_strong_password_invalid():
    with pytest.raises(ValidationError):
        django_forms.strong_password('abcdefg1')  # No uppercase
    with pytest.raises(ValidationError):
        django_forms.strong_password('ABCDEFG1')  # No lowercase
    with pytest.raises(ValidationError):
        django_forms.strong_password('Abcdefgh')  # No number
    with pytest.raises(ValidationError):
        django_forms.strong_password('Ab1')  # Too short

# --- utils/environment.py ---
def test_get_env_variable(monkeypatch):
    monkeypatch.setenv('MY_ENV_VAR', 'abc')
    assert environment.get_env_variable('MY_ENV_VAR') == 'abc'
    assert environment.get_env_variable('NOT_SET', 'default') == 'default'

def test_parse_comma_str_to_list():
    assert environment.parse_comma_str_to_list('a,b,c') == ['a', 'b', 'c']
    assert environment.parse_comma_str_to_list('  a , b , c  ') == ['a', 'b', 'c']
    assert environment.parse_comma_str_to_list('') == []
    assert environment.parse_comma_str_to_list(None) == []
    assert environment.parse_comma_str_to_list('"a, b, c"') == ['a', 'b', 'c']
    assert environment.parse_comma_str_to_list("'a, b, c'") == ['a', 'b', 'c']


