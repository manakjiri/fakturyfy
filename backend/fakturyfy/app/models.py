from django.db import models


class Entity(models.Model):
    name = models.CharField(max_length=150)
    abbreviation = models.CharField(max_length=7, blank=True)
    tax_number = models.CharField(max_length=15, blank=True)
    ic_number = models.IntegerField()
    address = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    bank_account = models.CharField(max_length=50)
    bank_code = models.CharField(max_length=4)
    bank_name = models.CharField(max_length=50, blank=True)
    note = models.TextField(blank=True)
    logo_filename = models.CharField(max_length=25, blank=True)

