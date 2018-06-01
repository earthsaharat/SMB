from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, date, time, timedelta
import json

class Profile(models.Model):
	name 		= models.CharField(max_length=50)
	image 		= models.ImageField(upload_to='img-profile/')
	create_date	= models.DateTimeField(default=timezone.now)
	creator		= models.ForeignKey('auth.User',on_delete=models.CASCADE)
	isEnable	= models.BooleanField(default=True)
	def lenDate(self):
		try:
			lastRecord = self.instruction_set.filter(isEnable=True).extra(
				select={'totalHour': '(day*24)+hour'},order_by = ['-totalHour'])[0]
			return {'day':lastRecord.day,'hour':lastRecord.hour,'minute':0}
		except Exception as e:
			return {'day':0,'hour':0,'minute':0}
		return {'day':0,'hour':0,'minute':0}
	def lenDateStr(self):
		aDate = Profile.lenDate(self)
		return str(aDate['day'])+'D '+str(aDate['hour'])+'H'
	def lenHour(self):
		aDate = Profile.lenDate(self)
		return aDate['day']*24 +aDate['hour']
	def usingDeviceCount(self):
		return len(list(self.device_set.filter(isEnable=True)))
	def __str__(self):
		return self.name

class Instruction(models.Model):
	profile 	= models.ForeignKey(Profile,on_delete=models.CASCADE)
	day			= models.IntegerField()
	hour		= models.IntegerField()
	temp 		= models.FloatField()
	humi 		= models.FloatField()
	r			= models.IntegerField()
	g			= models.IntegerField()
	b			= models.IntegerField()
	isEnable	= models.BooleanField(default=True)
	def __str__(self):
		return 'P'+str(self.profile.id)+'-'+str(self.day)+'D'+str(self.hour)+'H'

class Device(models.Model):
	name 		= models.CharField(max_length=50,default='no name')
	serial		= models.CharField(max_length=10,unique=True)
	user		= models.ForeignKey('auth.User',on_delete=models.CASCADE)
	profile 	= models.ForeignKey(Profile,on_delete=models.CASCADE)
	start_date	= models.DateTimeField(blank=True, null=True)
	isEnable	= models.BooleanField(default=True)
	# MARK : Status
	def getStatus(self):
		states = self.state_set.filter(isEnable=True).extra(order_by = ['-date'])
		if len(states) == 0:
			return {'date':None,'temp':None,'humi':None}
		aState = states[0]
		return {'date':aState.date,'temp':aState.temp,'humi':aState.humi}
	def getProgress(self):
		if self.getAllTimeInMinute() == 0: return None
		return format(min((self.getCurrentTimeInMinute()/self.getAllTimeInMinute())*100,100), '.2f')
	# MARK : Current Time
	def getCurrentTime(self):
		currentTime = timezone.now() - self.start_date
		return {'day'	:currentTime.days,
				'hour'	:int(currentTime.seconds/(60*60)),
				'minute':int(currentTime.seconds/60)%60}
	def getCurrentTimeStr(self):
		currentTime = Device.getCurrentTime(self)
		return str(currentTime['day'])+'D '+str(currentTime['hour'])+'H '+str(currentTime['minute'])+'M'
	def getCurrentTimeInMinute(self):
		currentTime = timezone.now() - self.start_date
		return (currentTime.days*24*60)+(int(currentTime.seconds/60)%60)
	def getCurrentTimeInHour(self):
		currentTime = timezone.now() - self.start_date
		return (currentTime.days*24)+int(currentTime.seconds/(60*60))
	# MARK : All Time
	def getAllTime(self):
		return self.profile.lenDate()
	def getAllTimeInMinute(self):
		return self.profile.lenHour() * 60
	def getAllTimeInHour(self):
		return self.profile.lenHour()
	# MARK : End Date
	def getEndDate(self):
		if self.start_date is None: return None
		allHour = self.profile.lenHour() 
		return self.start_date + timedelta(days=int(allHour/24), hours=int(allHour%24))
	# MARK : Instuction
	def getCurrentInstruction(self):
		instructions = self.profile.instruction_set.filter(isEnable=True).extra(
						select={'totalHour': '(day*24)+hour'},order_by = ['-totalHour'])
		currentHour = Device.getCurrentTimeInHour(self)
		for anInstruction in instructions:
			if anInstruction.totalHour <= currentHour:
				return anInstruction
		return Instruction(profile=self.profile,day=0,hour=0,temp=0,humi=0,r=0,g=0,b=0)
	def __str__(self):
		return str(self.serial)+'-'+self.user.username.upper()

class State(models.Model):
	device 		= models.ForeignKey(Device,on_delete=models.CASCADE)
	date		= models.DateTimeField(default=timezone.now)
	temp 		= models.FloatField()
	humi 		= models.FloatField()
	isEnable	= models.BooleanField(default=True)
	def __str__(self):
		return str(self.device)+'@'+timezone.localtime(self.date).strftime("%H:%M-%d/%m/%Y")