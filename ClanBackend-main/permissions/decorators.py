from functools import wraps
from .dynamic import DynamicPermission

from functools import wraps
from rest_framework.views import APIView


def apply_dynamic_permission(models=None):
    """
    Decorator to apply DynamicPermission to views or viewsets with specific models.
    :param models: Model or list of models to apply the permission to.
    """

    def decorator(view_class):
        original_permission_classes = view_class.permission_classes if hasattr(view_class, 'permission_classes') else []

        @wraps(view_class)
        def wrapped_view(*args, **kwargs):
            view_instance = view_class(*args, **kwargs)

            if models:
                if isinstance(models, list):
                    allowed_models = models
                else:
                    allowed_models = [models]

                class CustomDynamicPermission(DynamicPermission):
                    def has_permission(self, request, view):
                        model = getattr(view, 'queryset', None)
                        if model is not None:
                            model = model.model
                        elif hasattr(view, 'get_queryset'):
                            model = view.get_queryset().model

                        if model in allowed_models:
                            return super().has_permission(request, view)
                        return False

                view_instance.permission_classes = [CustomDynamicPermission] + list(original_permission_classes)

            return view_instance

        return wrapped_view

    return decorator
