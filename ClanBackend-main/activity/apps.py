from collections import OrderedDict

import django
from django.apps import apps
from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import pre_delete

from activity import settings as activity_settings
from activity.signals import action


class ActivityConfig(AppConfig):
    name = 'activity'
    default_auto_field = 'django.db.models.AutoField'
    verbose_name = 'Activity Streams'

    def ready(self):
        from activity.actions import action_handler
        action.connect(action_handler, dispatch_uid='activity.models')
        action_class = self.get_model('action')

        if activity_settings.USE_JSONFIELD:
            if not hasattr(action_class, 'data'):
                from activity.jsonfield import DataField
                DataField(blank=True, null=True).contribute_to_class(
                    action_class, 'data'
                )

        from activity.follows import delete_orphaned_follows
        pre_delete.connect(delete_orphaned_follows)
