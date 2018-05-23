# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Snapshots(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)  # Auto updated when data is inserted
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)  # Auto updated when data is altered

    picture = models.ImageField(upload_to='pictures')
    detected_faces = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.detected_faces


class AlertChoice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)  # Auto updated when data is inserted
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)  # Auto updated when data is altered

    alert_status = models.CharField(max_length=255)

    def __str__(self):
        return self.alert_status
