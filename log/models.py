"""
Log models
Mostafa Rasouli
mostafarasooli54@gmail.com
2023-11-29
"""

from django.db import models


class Log(models.Model):
    l_type = models.CharField(max_length=255, null=True, blank=True)
    endpoint = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    log = models.TextField(null=True, blank=True)
    ip = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.l_type} - {self.endpoint}'
