from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import json
import math

from django.utils import timezone
from datetime import datetime, date, time, timedelta

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from mcu import models as McuModels
from web import models as WebModels

# MARK : Date Method
def dateStr(input_date):
	if input_date is None: return None
	return timezone.localtime(input_date).strftime("%d/%m/%Y")
def dateTimeStr(input_date):
	if input_date is None: return None
	return timezone.localtime(input_date).strftime("%H:%M %d/%m/%Y")
# def endDate(start_date,length_hour):
# 	if start_date is None: return None
# 	return start_date + timedelta(days=int(length_hour/24), hours=int(length_hour%24))
# def lenDate(start_date,end_date):
# 	if start_date is None or end_date is None: return None
# 	final_date = end_date - start_date
# 	return {'day':final_date.days,'hour':int(final_date.seconds/(60*60)),'minute':int(final_date.seconds/60)%60}
# def lenHour(start_date,end_date):
# 	if start_date is None or end_date is None: return None
# 	final_date = end_date - start_date
# 	return (final_date.days*24)+int(final_date.seconds/(60*60))
# def lenMinute(start_date,end_date):
# 	if start_date is None or end_date is None: return None
# 	final_date = end_date - start_date
# 	return (final_date.days*24*60)+int(final_date.seconds/(60))


# MARK : MCU Service
def handleUpdate(request):
	if 	( 'serial' 	in request.GET ) and ( 'temp' 	in request.GET ) and ( 'humi' 	in request.GET ):
		try: adevice = McuModels.Device.objects.get(serial=request.GET['serial'])
		except: return HttpResponse('error')
		disableStatusSet = adevice.state_set.filter(isEnable=False)
		try: 
			flaot_temp = float(request.GET['temp'])
			flaot_humi = float(request.GET['humi'])
		except: return HttpResponse('error')
		if math.isnan(float(flaot_temp)) or math.isnan(float(flaot_humi)):
			return HttpResponse('error')
		if len(disableStatusSet) > 0:
			aState = disableStatusSet[0]
			aState.temp = flaot_temp
			aState.humi = flaot_humi
			aState.isEnable	= True
			aState.save()
		else:
			McuModels.State.objects.create(device=adevice,temp=flaot_temp,humi=flaot_humi)
		currentInstruction = adevice.getCurrentInstruction()
		return HttpResponse(
			str(int(currentInstruction.temp*10)).zfill(4)+"-"+
			str(int(currentInstruction.humi*10)).zfill(4)+"-"+
			str(int(currentInstruction.r)).zfill(3)+"-"+
			str(int(currentInstruction.g)).zfill(3)+"-"+
			str(int(currentInstruction.b)).zfill(3) )
	return HttpResponse('error')