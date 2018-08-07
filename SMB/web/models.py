from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

class GroupItem(models.Model):
	name 		= models.CharField(max_length=30)
	image 		= models.ImageField(upload_to='img-item/')
	def __str__(self):
		return self.name

class Item(models.Model):
	name 		= models.CharField(max_length=30)
	detail		= models.TextField(blank=True, null=True)
	cost 		= models.FloatField()
	group 		= models.ForeignKey(GroupItem,on_delete=models.CASCADE)
	def __str__(self):
		return self.name

class Order(models.Model):
	user 		= models.ForeignKey('auth.User',on_delete=models.CASCADE)
	image 		= models.ImageField(upload_to='img-slip/',blank=True, null=True)
	date		= models.DateTimeField(default=timezone.now)
	items		= models.TextField(default='[]')
	status_choice = (
		('0', 'รอการชำระเงิน'),
		('1', 'รอตรวจสอบการชำระเงิน'),
		('2', 'จัดส่งแล้ว') )
	status	 	= models.CharField(max_length=1, choices=status_choice)
	def __str__(self):
		return self.user