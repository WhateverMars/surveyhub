from django.urls import path
from django.contrib import admin

from . import old_views
from survey.views import EditorView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", old_views.index, name="index"),
    path("account", old_views.account, name="account"),
    path("register", old_views.register, name="register"),
    path("logout", old_views.logout_view, name="logout"),
    path("editor", EditorView.as_view(), name="editor"),
    path("results", old_views.results, name="results"),
    path("cleardata", old_views.cleardata, name="cleardata"),
]
