from unittest import TestCase

from django.apps.registry import apps


class ActivityConfigTestCase(TestCase):

    def test_data_field_is_added_to_action_class_only_once_even_if_app_is_loaded_again(self):
        activity_config = apps.get_app_config('activity')
        activity_config.ready()
        activity_config.ready()

        from activity.models import Action
        data_fields = [field for field in Action._meta.fields if field.name == 'data']
        self.assertEqual(
            len(data_fields),
            1
        )
