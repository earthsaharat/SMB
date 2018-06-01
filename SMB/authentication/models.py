from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

class Customer(models.Model):
	address		= models.TextField(blank=True, null=True)
	lineid		= models.CharField(max_length=20, blank=True, null=True)
	facebook	= models.CharField(max_length=50, blank=True, null=True)
	phone		= models.CharField(max_length=15, blank=True, null=True)
	user 		= models.ForeignKey('auth.User',on_delete=models.CASCADE)
	def __str__(self):
		return self.user