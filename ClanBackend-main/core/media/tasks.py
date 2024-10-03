from celery import shared_task
from .models import Media

@shared_task
def create_thumbnail(media_id):
    try:
        media = Media.objects.get(pk=media_id)
        media.generate_thumbnail()
        media.save()

    except Exception as e:
        print(e)