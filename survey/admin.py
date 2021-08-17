from django.contrib import admin

# Register your models here.
from .models import User, Surveyer, Result, Question, Analysis


admin.site.register(Surveyer)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(Analysis)
