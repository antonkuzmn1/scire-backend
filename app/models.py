# Copyright 2024 Anton Kuzmin (https://github.com/antonkuzmn1)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.contrib.auth.hashers import make_password
from django.db import models


class Company(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=255, default="")
    admins = models.ManyToManyField('Admin', related_name='companies')
    deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            if Company.objects.filter(username=self.username).exists():
                raise ValueError("Username already exists.")
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self): return self.name


class LDAP(models.Model):
    domain_component = models.CharField(max_length=50)
    base = models.CharField(max_length=50)
    common_name = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    title = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=255, default="")
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='ldaps')
    deleted = models.BooleanField(default=False)


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, default="")
    title = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=255, default="")
    since = models.DateField()
    tickets = models.IntegerField()
    last = models.DateField()
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='users')
    ldap = models.ForeignKey(
        LDAP,
        on_delete=models.CASCADE,
        related_name='users')
    deleted = models.BooleanField(default=False)


class Admin(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, default="")
    title = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=255, default="")
    since = models.DateField()
    tickets = models.IntegerField()
    last = models.DateField()
    companies = models.ManyToManyField(Company, related_name='admins')
    deleted = models.BooleanField(default=False)


class Message(models.Model):
    admin = models.ForeignKey(
        Admin,
        on_delete=models.CASCADE,
        related_name='messages_sent')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages_received')
    date = models.DateTimeField()
    text = models.CharField(max_length=255)


class Ticket(models.Model):
    admin = models.ForeignKey(
        Admin,
        on_delete=models.CASCADE,
        null=True, related_name='tickets')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tickets')
    start = models.DateTimeField()
    stop = models.DateField()
    type = models.ForeignKey(
        'Type',
        on_delete=models.CASCADE,
        related_name='tickets')


class Type(models.Model):
    text = models.CharField(max_length=50, primary_key=True)


class Note(models.Model):
    admin = models.ForeignKey(
        Admin,
        on_delete=models.CASCADE,
        related_name='notes')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notes')
    date = models.DateTimeField()
    text = models.CharField(max_length=255)
    deleted = models.BooleanField(default=False)
