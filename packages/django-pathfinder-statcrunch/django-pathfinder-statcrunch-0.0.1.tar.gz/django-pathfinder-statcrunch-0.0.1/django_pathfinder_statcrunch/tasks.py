from celery import task, shared_task
from .models import PathfinderUpload
from django_eveonline_connector.models import EveCharacter, PrimaryEveCharacterAssociation
import csv, logging 
logger = logging.getLogger(__name__)

@shared_task
def add_pathfinder_upload_to_report(upload_pk):
    upload = PathfinderUpload.objects.get(pk=upload_pk)
    report = upload.report.get_stats()
    if not report:
        report = {
            'characters': {},
            'corporations': {}
        }
    # parse report
  
    f = open(upload.file.path, 'r')
    for line in f:
        data = line.split(",")
        if len(data) != 57:
            logger.info(f"Skipping line in PF read: {line}")
            continue
        name = (data[2]).replace('"', "").strip()
        try:
            current_character = EveCharacter.objects.get(name=name)
            primary_character = current_character.get_primary_character(current_character.token.user)
            if primary_character:
                current_character = primary_character
        except Exception as e:
            logger.error(e)
            logger.warning(f"Skipping PF line, failed to find character for {name}")
            continue
        signatures = int(data[55].replace('"', "").strip())
        if current_character.name in report:
            report['characters'][current_character.name]['signatures'] += int(signatures)
        else:
            report['characters'][current_character.name] = {
                "signatures": int(signatures),
              "corporation": current_character.corporation.name,
            }

        if current_character.corporation.track_corporation:
            if current_character.corporation.name in report['corporations']:
                report['corporations'][current_character.corporation.name] += int(
                    signatures)
            else:
                report['corporations'][current_character.corporation.name] = int(
                    signatures)

    for key in report['corporations']:
        players = PrimaryEveCharacterAssociation.objects.filter(
            character__corporation__name=key)
        for player in players:
            primary_character = player.character 
            if primary_character.name not in report['characters']:
                report['characters'][primary_character.name] = {
                    'corporation': key,
                    'signatures': -1,
                }

    
        
    # update stats
    upload.report.update_stats(report)
    upload.delete()
