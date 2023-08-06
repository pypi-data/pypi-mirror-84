from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import PathfinderUpload
from .tasks import add_pathfinder_upload_to_report

@receiver(post_save, sender=PathfinderUpload)
def handle_pathfinder_upload(sender, **kwargs):
    def on_commit():
        instance = kwargs.get('instance')
        add_pathfinder_upload_to_report.apply_async(args=[instance.pk])

    transaction.on_commit(on_commit)