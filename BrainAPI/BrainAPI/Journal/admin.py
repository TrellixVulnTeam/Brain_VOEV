from django_neomodel import admin as neo_admin
from django.contrib import admin as dj_admin

from .models import Journal

class JournalAdmin(dj_admin.ModelAdmin):
    list_display = ("name", "name")
neo_admin.register(Journal, JournalAdmin)
