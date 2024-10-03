import uuid


def upload_to(instance, filename):
    if hasattr(instance, 'content_object'):
        model_name = instance.content_object.__class__.__name__.lower()
    else:
        model_name = instance.__class__.__name__.lower()

    extension = filename.split('.')[-1]
    unique_name = f"{uuid.uuid4()}.{extension}"
    return f"media/{model_name}/{unique_name}"
