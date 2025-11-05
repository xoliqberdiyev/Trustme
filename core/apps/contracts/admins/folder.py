from django.contrib import admin

from core.apps.contracts.models.folder import Folder


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']