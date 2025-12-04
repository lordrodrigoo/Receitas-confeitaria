import os
import pytest

# Load environment variables from .env for local test runs
# This keeps secrets out of the repository and makes fixtures read values
# from the developer's local environment automatically.
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from django.contrib.auth import get_user_model


@pytest.fixture
def admin_user(db):
    """Ensure an admin user exists, configured via environment variables.

    Reads `ADMIN_USERNAME` and `ADMIN_PASSWORD` from environment. This avoids
    hardcoding credentials in tests and allows CI to provide secrets securely.
    """
    User = get_user_model()
    # Do NOT use insecure defaults here. Require environment variables to be set.
    username = os.environ.get('ADMIN_USERNAME')
    password = os.environ.get('ADMIN_PASSWORD')
    if not username or not password:
        raise RuntimeError(
            'ADMIN_USERNAME and ADMIN_PASSWORD must be set in the environment (use a local .env file).'
        )
    user, created = User.objects.get_or_create(username=username, defaults={'email': 'admin@example.com'})
    if created or not user.check_password(password):
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
    return user
