from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = 'ar'
PARLER_DEFAULT_LANGUAGE_CODE = LANGUAGE_CODE
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LANGUAGES = (
    ("ar", _("Arabic")),
    ("en", _("English")),
)

PARLER_LANGUAGES = {
    None: (
        {'code': 'ar', 'name': _('Arabic')},
        {'code': 'en', 'name': _('English')},
    ),
    'default': {
        'fallbacks': ['ar'],
        'hide_untranslated': False,
    }
}

CITIES_LIGHT_TRANSLATION_LANGUAGES = ['ar', 'en']
CITIES_LIGHT_INCLUDE_COUNTRIES = ['SA']
CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC', 'PPLF', 'PPLG', 'PPLL', 'PPLR',
                                   'PPLS', 'STLMT', ]
# CITIES_LIGHT_APP_NAME = 'settings'
