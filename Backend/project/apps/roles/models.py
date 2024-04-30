from django.db import models

# Create your models here.
class Role(models.Model):
    role_name = models.CharField(max_length=75, blank=False, unique=True, null=False)
    description = models.TextField()

    def __str__(self):
        return self.role_name