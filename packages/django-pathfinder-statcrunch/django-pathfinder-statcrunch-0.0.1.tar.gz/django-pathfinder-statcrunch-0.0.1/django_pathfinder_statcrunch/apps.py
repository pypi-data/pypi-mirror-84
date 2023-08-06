from django.apps import AppConfig


class DjangoPathfinderStatcrunchConfig(AppConfig):
    name = 'django_pathfinder_statcrunch'
    url_slug = 'pathfinder'

    def ready(self):
        from django.db.models.signals import post_save
        from .models import PathfinderUpload
        from .signals import handle_pathfinder_upload

        post_save.connect(handle_pathfinder_upload, sender=PathfinderUpload)