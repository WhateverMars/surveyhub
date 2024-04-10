"""
surveyhub URL Configuration
"""
from django.urls import include, path

urlpatterns = [
    path('', include('survey.urls'))
]
