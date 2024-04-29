from django.db import models

# Create your models here.
class Permission(models.Model):
    permission_name = models.CharField(max_length=75, blank=False, null=False)
    description = models.TextField(blank=True)