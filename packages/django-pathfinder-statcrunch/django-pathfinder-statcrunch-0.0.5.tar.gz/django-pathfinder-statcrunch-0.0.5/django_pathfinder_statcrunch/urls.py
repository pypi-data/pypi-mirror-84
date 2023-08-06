from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from . import views 

# SSO
urlpatterns = [
    path('reports/', views.list_reports,
         name="django-pathfinder-statcrunch-list-reports"),
    path('reports/<int:pk>/', views.view_report,
        name="django-pathfinder-statcrunch-view-report"),
    path('reports/<int:pk>/refresh/', views.refresh_report,
         name="django-pathfinder-statcrunch-view-report-refresh"),
]
