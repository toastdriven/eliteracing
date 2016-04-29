from .settings import *

# Don't run the migrations when running tests, for speed & count sanity.
class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"

MIGRATION_MODULES = DisableMigrations()

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
