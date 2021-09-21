from django.db import models
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
