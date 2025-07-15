from django.contrib import admin

from core.apps.shared.models.folder import Folder


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']