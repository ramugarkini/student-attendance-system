# auth/models.py
from django.db import models

class ConfigurationSettings(models.Model):
    id = models.BigAutoField(primary_key=True)
    rows_per_page = models.PositiveIntegerField(default=10, null=True)
    topbar_link = models.CharField(max_length=255, blank=True, null=True)
    topbar_link_text = models.CharField(max_length=255, blank=True, null=True)
    sidebar_text = models.CharField(max_length=255, blank=True, null=True)
    sidebar_icon = models.ImageField(upload_to='images/icons/', blank=True, null=True)
    favicon = models.ImageField(upload_to='images/icons/', blank=True, null=True)
    user_icon = models.ImageField(upload_to='images/icons/', blank=True, null=True)
    server_user_name = models.CharField(max_length=255, blank=True, null=True)
    client_user_name = models.CharField(max_length=255, blank=True, null=True)
    
    ALLOW_ACCESS_CHOICES = [
        (False, 'Off'),
        (True, 'On'),
    ]
    allow_access = models.BooleanField(choices=ALLOW_ACCESS_CHOICES, default=False)

    def __str__(self):
        return f'Configuration Settings - ID: {self.id}'

