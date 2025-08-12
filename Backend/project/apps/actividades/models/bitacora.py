from django.db import models

# RELACION
from apps.users.models import User

# Tiempo
from django.utils import timezone

class LogLevel(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100)
    priority = models.IntegerField(help_text="Prioridad (menor número = más importante)")

    def __str__(self):
        return self.name

class LogCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    action = models.CharField(max_length=100)
    details = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(LogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.timestamp} - {self.user}: {self.action}"

class SystemLog(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    level = models.ForeignKey(LogLevel, on_delete=models.PROTECT)
    source = models.CharField(max_length=100)
    message = models.TextField()
    category = models.ForeignKey(LogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    traceback = models.TextField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['level']),
            models.Index(fields=['source']),
        ]

    def __str__(self):
        return f"{self.timestamp} - {self.level}: {self.message[:100]}"