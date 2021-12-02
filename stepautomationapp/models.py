from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from PIL import Image


class UserData(models.Model):
    userrelation = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=225, null=True, blank=True)
    city = models.CharField(max_length=225, null=True, blank=True)
    profilepic = models.ImageField(upload_to='media', default='media/profilepic.png')
    address = models.TextField(null=True, blank=True)
    zipcode = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return self.userrelation


class UserFiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projectName = models.CharField(max_length=225)
    customerName = models.CharField(max_length=225)
    description = models.TextField()
    userFile = models.FileField(upload_to='userfiles')


class Country(models.Model):
    country = models.CharField(max_length=225)

    def __str__(self):
        return self.country


class City(models.Model):
    countryrel = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.CharField(max_length=225)

    def __str__(self):
        return self.city


class Steps(models.Model):
    user = models.CharField(max_length=225)
    step_name = models.CharField(max_length=225)
    step_count = models.IntegerField()
    step_description = models.TextField()
    step_visibility = models.CharField(max_length=20)
    step_download = models.CharField(max_length=20)
    step_document = models.FileField(upload_to='stepfiles')


class Documents(models.Model):
    user = models.CharField(max_length=225)
    description = models.CharField(max_length=225)
    step_document = models.FileField(upload_to='documents')
    notarize = models.CharField(max_length=10)
    apostille = models.CharField(max_length=10)
    file_add_date = models.DateTimeField(auto_now=True)


class Customers(models.Model):
    user = models.CharField(max_length=225)
    customer_name = models.CharField(max_length=225)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    email = models.EmailField(max_length=225)
    location = models.CharField(max_length=225)
    customer_added_date = models.DateTimeField(auto_now=True)
