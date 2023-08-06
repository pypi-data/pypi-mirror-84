from django.shortcuts import render, redirect
from .models import MonthlyReport, PathfinderUpload
from django_eveonline_connector.models import PrimaryEveCharacterAssociation, EveCharacter
import logging 
logger = logging.getLogger(__name__)
# Create your views here.
def list_reports(request):
    return render(request, 'django_pathfinder_statcrunch/adminlte/list_reports.html', context={
        "reports": MonthlyReport.objects.all()
    })

def refresh_report(request, pk):
    uploads = PathfinderUpload.objects.filter(report__pk=pk)
    for upload in uploads:
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
                primary_character = current_character.get_primary_character(
                    current_character.token.user)
                if primary_character:
                    current_character = primary_character
            except Exception as e:
                logger.error(e)
                logger.warning(
                    f"Skipping PF line, failed to find character for {name}")
                continue
            signatures = int(data[55].replace('"', "").strip())
            if current_character.name in report:
                report['characters'][current_character.name]['signatures'] += int(
                    signatures)
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
    
    return redirect('django-pathfinder-statcrunch-view-report', pk)

def view_report(request, pk):
    context = {}
    report = MonthlyReport.objects.get(pk=pk)
    context['characters'] = report.get_stats()['characters']
    context['corporations'] = {}
    context['pk'] = pk 
    for key in report.get_stats()['corporations']:
        player_count = PrimaryEveCharacterAssociation.objects.filter(
            character__corporation__name=key).count()
        context['corporations'][key] = {
            'signatures': report.get_stats()['corporations'][key],
            'signatures_per_capita': report.get_stats()['corporations'][key] / player_count,
        }
    return render(request, 'django_pathfinder_statcrunch/adminlte/view_report.html', context=context)
