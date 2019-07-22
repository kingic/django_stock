from django.contrib import admin

from .models import Question, Search
# Register your models here.

admin.site.register(Question)
admin.site.register(Search)
