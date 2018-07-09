# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Snapshots, AlertChoice, AlertRecord


# Register your models here.
admin.site.register(AlertRecord)


class SnapshotsAdmin(admin.ModelAdmin):
    # define which columns should be displayed
    list_display = ('id', 'created_at', 'picture', 'video')

    ordering = ('-id',)


# This will register my models to admin
admin.site.register(Snapshots, SnapshotsAdmin)
# Note: To enable list_display I have to register admin-name too
