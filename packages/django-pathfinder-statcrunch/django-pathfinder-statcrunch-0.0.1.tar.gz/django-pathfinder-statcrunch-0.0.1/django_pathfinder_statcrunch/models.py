from django.db import models
from django.contrib.auth.models import User 
from datetime import datetime
import json

class PathfinderUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.ForeignKey("MonthlyReport", on_delete=models.CASCADE)
    file = models.FileField()

class MonthlyReport(models.Model):
    date = models.DateField(auto_now=True)
    statistics = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.date.strftime("%B %Y")

    def save(self, *args, **kwargs):
        if MonthlyReport.objects.filter(date__startswith=datetime.now().strftime('%Y-%m-')).exists():
            report = MonthlyReport.objects.get(date__startswith=datetime.now().strftime('%Y-%m-'))
            if report.pk != self.pk:
                raise Exception("Report exists")
        super(MonthlyReport, self).save(*args, **kwargs)

    def get_stats(self):
        if not self.statistics:
            return json.loads("{}")
        return json.loads(self.statistics)

    def update_stats(self, report):
        self.statistics = json.dumps(report)
        self.save()
