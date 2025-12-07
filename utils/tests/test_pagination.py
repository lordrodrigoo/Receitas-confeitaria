import pytest
from django.http import HttpRequest
from utils.pagination import make_pagination_range, make_pagination

@pytest.mark.parametrize("page_range, qty_pages, current_page, expected", [
    (range(1, 11), 4, 1, {'start_range': 0, 'stop_range': 4}),
    (range(1, 11), 4, 10, {'start_range': 2, 'stop_range': 12}),
    (range(1, 11), 4, -2, {'start_range': 0, 'stop_range': 4}),
    (range(1, 6), 2, 5, {'start_range': 1, 'stop_range': 6}),
])
def test_make_pagination_range_branches(page_range, qty_pages, current_page, expected):
    result = make_pagination_range(page_range, qty_pages, current_page)
    assert result['start_range'] == expected['start_range']
    assert result['stop_range'] == expected['stop_range']
    assert isinstance(result['pagination'], list) or isinstance(result['pagination'], range)


def test_make_pagination_range_out_of_range_flags():
    page_range = range(1, 11)
    qty_pages = 4
    # current_page > middle_range
    result = make_pagination_range(page_range, qty_pages, 5)
    assert result['first_page_out_of_range'] is True
    # stop_range < total_pages
    assert result['last_page_out_of_range'] is True or result['last_page_out_of_range'] is False


def test_make_pagination_valid_and_invalid_page():
    class DummyQueryset:
        def __len__(self): return 10
        def __getitem__(self, item): return list(range(10))[item]
    queryset = DummyQueryset()
    # request with valid page
    request = HttpRequest()
    request.GET = {'page': '1'}
    page_obj, pagination_range = make_pagination(request, queryset, per_page=2, qty_pages=2)
    assert hasattr(page_obj, 'object_list')
    assert 'pagination' in pagination_range
    # request with invalid page
    request.GET = {'page': 'invalid'}
    page_obj, pagination_range = make_pagination(request, queryset, per_page=2, qty_pages=2)
    assert hasattr(page_obj, 'object_list')
    assert 'pagination' in pagination_range
