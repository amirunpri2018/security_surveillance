# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Snapshots, AlertChoice


# Register your models here.


class SnapshotsAdmin(admin.ModelAdmin):
    # define which columns should be displayed
    list_display = ('id', 'created_at', 'picture', 'detected_faces')

    # add search field
    search_fields = ['detected_faces', ]

    ordering = ('id',)

admin.site.register(Snapshots, SnapshotsAdmin)  # This will register my models to admin
# Note: To enable list_display I have to register admin-name too