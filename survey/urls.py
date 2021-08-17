from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('account', views.account, name='account'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('editor', views.editor, name='editor'),
    path('results', views.results, name='results'),
    path('cleardata', views.cleardata, name='cleardata')
]