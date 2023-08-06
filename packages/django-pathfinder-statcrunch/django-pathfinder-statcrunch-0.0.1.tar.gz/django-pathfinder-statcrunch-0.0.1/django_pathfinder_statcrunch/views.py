from django.shortcuts import render
from .models import MonthlyReport
from django_eveonline_connector.models import PrimaryEveCharacterAssociation

# Create your views here.
def list_reports(request):
    return render(request, 'django_pathfinder_statcrunch/adminlte/list_reports.html', context={
        "reports": MonthlyReport.objects.all()
    })

def view_report(request, pk):
    context = {}
    report = MonthlyReport.objects.get(pk=pk)
    context['characters'] = report.get_stats()['characters']
    context['corporations'] = {}
    for key in report.get_stats()['corporations']:
        player_count = PrimaryEveCharacterAssociation.objects.filter(
            character__corporation__name=key).count()
        context['corporations'][key] = {
            'signatures': report.get_stats()['corporations'][key],
            'signatures_per_capita': report.get_stats()['corporations'][key] / player_count,
        }
    return render(request, 'django_pathfinder_statcrunch/adminlte/view_report.html', context=context)
