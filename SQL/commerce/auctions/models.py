from pyexpat import model
from statistics import mode
from turtle import title
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
   pass

class Listing(models.Model):
   title = models.CharField(max_length=64)
   seller_name = models.CharField(max_length=64)
   description = models.TextField()
   bid_start = models.IntegerField()
   category = models.CharField(max_length=64)
   image_url = models.CharField(max_length=200, default=None, blank=True, null=True)
   created_time = models.DateTimeField(auto_now_add=True)

class Bid(models.Model):
   user = models.CharField(max_length=64)
   title = models.CharField(max_length=64)
   bid_id = models.IntegerField()
   bid = models.IntegerField()

class Comment(models.Model):
   user = models.CharField(max_length=64)
   commet = models.CharField(max_length=64)
   bid_id = models.IntegerField()
   tempstamp = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
   user = models.CharField(max_length=64)
   bid_id = models.IntegerField()

class Winner(models.Model):
   title = models.CharField(max_length=64, null=True)
   owner = models.CharField(max_length=64)
   winner = models.CharField(max_length=64)
   bid_id = models.IntegerField()
   final_prize = models.IntegerField()