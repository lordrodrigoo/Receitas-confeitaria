import importlib
import sys
import os
import pytest

@pytest.mark.parametrize('engine,expected_engine', [
    ('django.db.backends.postgresql', 'django.db.backends.postgresql'),
    ('django.db.backends.sqlite3', 'django.db.backends.sqlite3'),
])
def test_database_settings(monkeypatch, engine, expected_engine):
    monkeypatch.setenv('DATABASE_ENGINE', engine)
    monkeypatch.setenv('DATABASE_NAME', 'test_db')
    monkeypatch.setenv('DATABASE_USER', 'test_user')
    monkeypatch.setenv('DATABASE_PASSWORD', 'test_pass')
    monkeypatch.setenv('DATABASE_HOST', 'test_host')
    monkeypatch.setenv('DATABASE_PORT', '1234')
    
    # Remove module from sys.modules to force reload
    sys.modules.pop('project.settings.databases', None)
    db_settings = importlib.import_module('project.settings.databases')
    assert db_settings.DATABASES['default']['ENGINE'] == expected_engine
    assert db_settings.DATABASES['default']['NAME'] == 'test_db'
    if engine == 'django.db.backends.postgresql':
        assert db_settings.DATABASES['default']['USER'] == 'test_user'
        assert db_settings.DATABASES['default']['PASSWORD'] == 'test_pass'
        assert db_settings.DATABASES['default']['HOST'] == 'test_host'
        assert db_settings.DATABASES['default']['PORT'] == '1234'
