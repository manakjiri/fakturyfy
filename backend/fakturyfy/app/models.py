from django.db import models


class Entity(models.Model):
    """
    Entity represents a company or a person that is a part of the invoice.

    name: address header line - name of addressee or company name
    abbreviation: abbreviation of the company name (used in file paths)
    address: line of the address with street and house number
    city: city or part of the city
    zip_code: zip code (PSČ in Czech)
    country: country
    phone:
    email:
    bank_name:
    bank_account: bank account number
    bank_code:
    note: note that will be written on the invoice
    vat_id: value added tax identification number (DIČ in czech)
    vat_note: VAT note
    ic_number: Taxpayer identification Number (IČO in czech)
    logo_filename: path to the image of logo of the company
    """

    name = models.CharField(max_length=150)
    abbreviation = models.CharField(max_length=50, unique=True)
    ic_number = models.IntegerField()
    tax_number = models.CharField(max_length=15, blank=True)
    tax_note = models.TextField(blank=True)
    address = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    bank_account = models.CharField(max_length=50)
    bank_code = models.CharField(max_length=4, blank=True)
    bank_name = models.CharField(max_length=50, blank=True)
    logo = models.ImageField(upload_to='logos', blank=True, null=True)

