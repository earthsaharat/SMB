from django.shortcuts import render
from django.shortcuts import redirect
import json

from django.utils import timezone
from datetime import datetime, date, time, timedelta

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from mcu import models as McuModels
from web import models as WebModels

from mcu import views as McuViews

# MARK : ERROR
def admin_error(request):
	return error(request,'page not found')
def error(request,message):
	return render(request,'admin_error.html',{'error':message})

# MARK : Admin Site
def admin_check(user):
	if not user.is_staff: return False
	return True

@login_required
@user_passes_test(admin_check)
def admin_home(request):
	return render(request,'admin_home.html',
		{	'len_order'		:len(WebModels.Order.objects.all()),
			'len_profile'	:len(McuModels.Profile.objects.filter(isEnable=True)),
			'len_device'	:len(McuModels.Device.objects.filter(isEnable=True)) })


@login_required
@user_passes_test(admin_check)	
def admin_order(request):
	orders = []
	for aorder in WebModels.Order.objects.all():
		orders.append({})
	return render(request,'order/home.html',{'orders':orders})

@login_required
@user_passes_test(admin_check)	
def admin_profile(request):
	profiles = []
	for profile in McuModels.Profile.objects.filter(isEnable=True):
		profiles.append({	'id'		:profile.id,
							'name'		:profile.name,
							'lenDate'	:profile.lenDate(),
							'inUseCount':profile.usingDeviceCount(),
							'image'		:str(profile.image),
							'creator'	:profile.creator.first_name})
	return render(request,'profile/home.html',{'profiles':json.dumps(profiles)})


@login_required
@user_passes_test(admin_check)	
def admin_profile_edit(request,id):
	try: aprofile = McuModels.Profile.objects.get(id=id)
	except: return error(request,'profile not found')
	if request.method == 'POST':
		aprofile.name 	= request.POST['name']
		if 'imageInput' in request.FILES:
			aprofile.image 	= request.FILES['imageInput']
		# aprofile.data = json.dumps(sorted(allActions,key=lambda k:int(k['hour'])+int(k['day'])*24))
		aprofile.save()
		allActions = json.loads(request.POST['content'])
		allActions = sorted(allActions,key=lambda k:int(k['hour'])+int(k['day'])*24)
		for aInstruction in McuModels.Instruction.objects.filter(profile=aprofile):
			if len(allActions) != 0:
				anAction = allActions.pop(0)
				aInstruction.day	= anAction['day']
				aInstruction.hour	= anAction['hour']
				aInstruction.temp	= anAction['temp']
				aInstruction.humi	= anAction['humi']
				aInstruction.r		= anAction['r']
				aInstruction.g		= anAction['g']
				aInstruction.b		= anAction['b']
				aInstruction.isEnable = True
			else:
				aInstruction.isEnable = False
			aInstruction.save()
		for anAction in allActions:
			McuModels.Instruction.objects.create(
				profile = aprofile,
				day		= anAction['day'],
				hour	= anAction['hour'],
				temp	= anAction['temp'],
				humi	= anAction['humi'],
				r		= anAction['r'],
				g		= anAction['g'],
				b		= anAction['b'] )
	# data = aprofile.data
	data = json.dumps( 
		list(aprofile.instruction_set.filter(isEnable=True).values('day','hour','temp','humi','r','g','b')) )
	return render(request,'profile/edit.html',{'name':aprofile.name,'data':data,'image':aprofile.image})

@login_required
@user_passes_test(admin_check)	
def admin_profile_add(request):
	if request.method == 'POST':
		name = request.POST['name']
		aprofile = McuModels.Profile.objects.create(name=name,creator=request.user)
		return redirect('admin_profile_edit',id=aprofile.id)
	return render(request,'profile/add.html')

@login_required
@user_passes_test(admin_check)	
def admin_device(request):
	datas = []
	for adevice in McuModels.Device.objects.all():

		try: last_update = McuModels.State.objects.filter(device=adevice).latest('date')
		except: last_update = None

		try: day = (last_update-adevice.start_date)
		except: day = None

		datas.append({	'id'			:adevice.id,
						'name'			:adevice.name,
						'serial'		:adevice.serial,
						'user'			:adevice.user.first_name,
						'profile'		:adevice.profile,
						'status'		:'None',
						'start_date'	:McuViews.dateTimeStr(adevice.start_date),
						'current_time'	:adevice.getCurrentTimeStr(),
						'last_update'	:timezone.localtime(adevice.getStatus()['date']).strftime("%H:%M %d/%m/%Y"),
						'day'			:day })
	return render(request,'device/home.html',{'data':datas})

@login_required
@user_passes_test(admin_check)	
def admin_device_edit(request,id):

	allUser = []
	for auser in User.objects.all(): allUser.append({'id':auser.id,'name':auser.first_name})
	allProfile = []
	for aprofile in McuModels.Profile.objects.filter(isEnable=True): 
		allProfile.append({'id':aprofile.id,'name':aprofile.name})
	try: 
		adevice = McuModels.Device.objects.get(id=id)
		isNewDevice = False
	except: isNewDevice = True

	if request.method == 'POST':
		# MARK : Serial
		new_serial = request.POST['serial']
		if len(new_serial) == 0: return error(request,'no serial')
		serialAllDevice = McuModels.Device.objects.filter(serial=new_serial)
		for aSerialDevice in serialAllDevice:
			if aSerialDevice.id != adevice.id: return error(request,'This serial already exists')
		# MARK : Name
		new_name = request.POST['name']
		if new_name == '': new_name = 'no name'
		# MARK : User
		try: new_user = User.objects.get(id=int(request.POST['owner']))
		except: return error(request,'ERROR! user not found')
		# MARK : Profile
		try: new_profile = McuModels.Profile.objects.get(id=int(request.POST['profile']))
		except: return error(request,'ERROR! profile not found')
		# MARK : Start Date
		new_start_date = request.POST['start_date']
		if new_start_date == '': new_start_date = None
		else: new_start_date = datetime.strptime(new_start_date,"%Y-%m-%dT%H:%M")
		# MARK : SAVE
		if isNewDevice:
			adevice = McuModels.Device.objects.create(
				serial 		= new_serial,
				name 		= new_name,
				user 		= new_user,
				profile 	= new_profile,
				start_date 	= new_start_date)
		else:
			adevice.serial 		= new_serial
			adevice.name 		= new_name
			adevice.user 		= new_user
			adevice.profile 	= new_profile
			adevice.start_date 	= new_start_date
			adevice.save()
		return redirect('admin_device')

	if isNewDevice:
		data = { 	'serial':'',
					'id':'',
					'name':'',
					'user':request.user,
					'profile':'',
					'start_date':'',
					'status':None }
	else:
		data = {	'serial':adevice.serial,
					'id':adevice.id,
					'name':adevice.name,
					'user':adevice.user.id,
					'profile':adevice.profile.id,
					'start_date':timezone.localtime(adevice.start_date).strftime("%Y-%m-%dT%H:%M"),
					'status':'ready' }
	
	return render(request,'device/edit.html',{'data':data,'alluser':allUser,'allprofile':allProfile})

@login_required
@user_passes_test(admin_check)	
def admin_device_remove(request,id):
	try: 
		adevice = McuModels.Device.objects.get(id=id)
	except: return error(request,'ERROR! device not found')
	# adevice.delete()
	adevice.isEnable = False
	adevice.save()
	return redirect('admin_device')