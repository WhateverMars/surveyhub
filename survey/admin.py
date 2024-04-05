from django.contrib import admin

# Register your models here.
from .models import User, Surveyor, Result, Question, Analysis


admin.site.register(Surveyor)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(Analysis)
