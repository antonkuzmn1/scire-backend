from django.contrib.auth.hashers import check_password, make_password
from django.db import models


class Company(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=255, default="")
    deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            if Company.objects.filter(username=self.username).exists():
                raise ValueError("Username already exists.")
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
