from .environment import BASE_DIR

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'base_static']
STATIC_ROOT = BASE_DIR / 'static'


# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
