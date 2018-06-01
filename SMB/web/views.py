# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
# from django.shortcuts import render, redirect
# # from crispy_forms.utils import render_crispy_form
# from django.views.generic.edit import FormView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.views.generic.list import ListView
# from django.http import HttpResponseRedirect,HttpResponse
# from django.contrib import messages
# from . import models
# import json
# # from AppControl.models import Profile,UpdateProfileBoxModelForm

from django.shortcuts import render
from django.shortcuts import redirect
import json

from django.utils import timezone
from datetime import datetime, date, time, timedelta

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from colorsys import rgb_to_hls

from mcu import models as McuModels
from web import models as WebModels

from mcu import views as McuViews

# MARK : User Site

#@login_required
def home( request):
	# username,mail = request.user.username.split("@")
	username= request.user.username
	return render(request, 'web_home.html',{'username':username})

def buy_box(request):
	# buyform = BuyBoxModelForm()
	# if request.method == 'POST':
	# 	buyform = BuyBoxModelForm(request.POST, request.FILES)
	# 	if buyform.is_valid():
	# 		buy_obj = Buy.objects.create(
	# 			name=buyform.cleaned_data['name'],
	# 			address = buyform.cleaned_data['address'],
	# 			email = buyform.cleaned_data['email'],
	# 			phone_number = buyform.cleaned_data['phone_number'],
	# 			order_amount = buyform.cleaned_data['order_amount'],
	# 			)
	# 		messages.success(request, 'คุณได้สั่งซื้อเรียบร้อยแล้ว', extra_tags='alert')
	# 		return HttpResponseRedirect('/mushroom/buy/success')
	# 	else:
	# 		print("not valid")
	# 		messages.error(request, "Error")
	# return render(request, 'buy.html',{'buyform':buyform,'form':DocumentForm2(),
	# 'buyformmushroom':BuyMushroomModelForm()})
	return render(request, 'buy.html')

def web_contact(request):
	return render(request, 'web_contact.html')
	# return render(request, 'old/moredetail.html')

def web_product(request):
	return redirect('/')
	# groupItems = models.GroupItem.objects.all()
	# try:
	# 	anOrder = models.Order.objects.get(user=request.user)
	# 	total = 0
	# 	for item in json.loads(anOrder.items):
	# 		total += (models.Item.objects.get(id=item)).cost
	# except:
	# 	total = 0
	# 	anOrder = None
	# data = {}
	# for group in groupItems:
	# 	data[group.name] = {'item':[],'image':group.image}
	# 	for item in models.Item.objects.filter(group=group):
	# 		data[group.name]['item'].append({
	# 			'id':item.id,
	# 			'name':item.name,
	# 			'cost':int(item.cost),
	# 			'selected': item.id in json.loads(anOrder.items) if anOrder != None else False })
	# return render(request, 'web_product.html',{'data':data,'total':int(total)})

def web_profile(request):
	profiles = []
	profilesid = []
	for aprofile in McuModels.Profile.objects.filter(isEnable=True):
		inUseCount = len(McuModels.Device.objects.filter(profile=aprofile))
		profiles.append({	'id'		:aprofile.id,
							'name'		:aprofile.name,
							'lenDate'	:aprofile.lenDate(),
							'inUseCount':inUseCount,
							'image'		:str(aprofile.image),
						})
		profilesid.append(aprofile.id)
	return render(request, 'web_profile/home.html',{'profiles':profiles,'profilesid':json.dumps(profilesid)})

@login_required
def web_add_remove(request,itemid):
	try:
		anOrder = models.Order.objects.get(user=request.user)
	except:
		anOrder = models.Order.objects.create(user=request.user)
	items = json.loads(anOrder.items)
	try:
		item = models.Item.objects.get(id=itemid)
	except:
		return redirect('web_product')
	if itemid in items:
		items.remove(itemid)
	else:
		items.append(itemid)
	anOrder.items = json.dumps(items)
	anOrder.save()
	return redirect('web_product')

@login_required
def web_mybox(request):
	devices = []
	devicesID = []

	# try: last_update = McuModels.State.objects.filter(device=adevice).latest('date')
	# except: last_update = None

	for adevice in McuModels.Device.objects.filter(user=request.user):
		if adevice.start_date is not None:
			# end_date = McuViews.endDate(adevice.start_date,adevice.profile.lenHour())

			end_date 		= adevice.getEndDate()
			anInstruction 	= adevice.getCurrentInstruction()
			currentStatus 	= adevice.getStatus()

			# if adevice.start_date == end_date:
			# 	progress = 100
			# else:
			# 	progress = 	int((McuViews.lenMinute(adevice.start_date,update_date)/
			# 				McuViews.lenMinute(adevice.start_date,end_date))*100)

			# if progress > 100: progress = 100
			# time_left = McuViews.lenDate(update_date,end_date)
			# isFinished = time_left['day']*24+time_left['hour'] < 0
			# status = 'finished' if isFinished else 'running'

			progress 		= adevice.getProgress()
			isFinished 		= progress == 100
			status 			= ''
			if progress == 100: 	status = 'Finished'
			elif progress == None: 	status = 'Unknow'
			else: 					status = 'Running'

			devices.append({	'id'		:adevice.id,
								'serial'	:adevice.serial,
								'name'		:adevice.name,
								'profile'	:adevice.profile.name,
								'status'	:status,
								'temp'		:str(currentStatus['temp'])+'/'+str(anInstruction.temp)+'°c',
								'humi'		:str(currentStatus['humi'])+'/'+str(anInstruction.humi)+'%',
								'light'		:'OFF' if 	anInstruction.r == 0 and
														anInstruction.g == 0 and
														anInstruction.b == 0 else 'ON',
								'progress'		:progress ,
								'start_date'	:McuViews.dateStr(adevice.start_date),
								'update_date'	:McuViews.dateStr(currentStatus['date']),
								'end_date'		:McuViews.dateStr(end_date), })
		else:
			devices.append({	'id'		:adevice.id,
								'serial'	:adevice.serial,
								'name'		:adevice.name,
								'profile'	:adevice.profile.name,
								'status'	:'stoped',
								'temp'		:None,
								'humi'		:None,
								'light'		:None,
								'progress'		:None ,
								'start_date'	:None,
								'update_date'	:None,
								'end_date'		:None, })
		devicesID.append(adevice.id)
	return render(request, 'mybox/home.html',{'boxs':devices,'boxsid':json.dumps(devicesID)})

@login_required
def web_mybox_view(request,id):

	try: adevice = McuModels.Device.objects.get(id=id,user=request.user)
	except: return redirect('web_product')	

	if adevice.start_date is not None:
		end_date 		= adevice.getEndDate()
		anInstruction 	= adevice.getCurrentInstruction()

		time_all		= adevice.getAllTime()
		time_use		= adevice.getCurrentTime()
		time_left		= adevice.start_date - end_date
		time_left		= {	'day' 	:max(0,time_left.days),
							'hour'	:max(0,int(time_left.seconds/(60*60))),
							'minute':max(0,int(time_left.seconds/60)%60) }

		currentStatus 	= adevice.getStatus()
		progress 		= adevice.getProgress()
		isFinished 		= progress == 100
		status 			= ''
		if progress == 100: 	status = 'Finished'
		elif progress == None: 	status = 'Unknow'
		else: 					status = 'Running'

		aBox = 			{	'id'		:adevice.id,
							'serial'	:adevice.serial,
							'name'		:adevice.name,
							'profile'	:adevice.profile.name,
							'status'	:status,
							'temp'		:str(currentStatus['temp'])+'/'+str(anInstruction.temp)+'°c',
							'humi'		:str(currentStatus['humi'])+'/'+str(anInstruction.humi)+'%',
							'light'		:'rgb('	+str(anInstruction.r)+','
												+str(anInstruction.g)+','
												+str(anInstruction.b)+')',
							'time_all'	:time_all,
							'time_use'	:time_use,
							'time_left'	:time_left,
							'progress'		:progress,
							'start_date'	:McuViews.dateTimeStr(adevice.start_date),
							'update_date'	:McuViews.dateTimeStr(currentStatus['date']),
							'end_date'		:McuViews.dateTimeStr(end_date), }
	else:
		aBox = 			{	'id'		:adevice.id,
							'serial'	:adevice.serial,
							'name'		:adevice.name,
							'profile'	:adevice.profile.name,
							'status'	:'stoped',
							'temp'		:None,
							'humi'		:None,
							'light'		:'rgb(0,0,0)',
							'time_all'	:{'day':None,'hour':None,'minute':None},
							'time_use'	:{'day':None,'hour':None,'minute':None},
							'time_left'	:{'day':None,'hour':None,'minute':None},
							'progress'		:None ,
							'start_date'	:None,
							'update_date'	:None,
							'end_date'		:None, }
	return render(request, 'mybox/view.html',{'box':aBox})

@login_required
def web_mybox_edit(request,id):
	try: adevice = McuModels.Device.objects.get(id=id,user=request.user)
	except: return redirect('web_mybox')

	if request.method == 'POST':
		adevice.name 	= request.POST['name'] if request.POST['name'] != "" else "no name"
		# try: auser = User.objects.get(id=int(request.POST['owner']))
		# except: return error(request,'ERROR! user not found')
		# adevice.user = auser
		try: aprofile = McuModels.Profile.objects.get(id=int(request.POST['profile']))
		except: return redirect('web_mybox')
		adevice.profile = aprofile
		adevice.save()
		return redirect('web_mybox')

	box = {	'id'		:adevice.id, 
			'name'		:adevice.name,
			'serial'	:adevice.serial,
			'profile'	:adevice.profile.id,
			'start_date':McuViews.dateTimeStr(adevice.start_date),
			'end_date'	:McuViews.dateTimeStr(adevice.getEndDate()) }
	allProfile = []
	for aprofile in McuModels.Profile.objects.filter(isEnable=True): 
		allProfile.append({'id':aprofile.id,'name':aprofile.name})
	return render(request, 'mybox/edit.html',{'box':box,'allprofile':allProfile})

@login_required
def web_mybox_action(request,id):
	try: adevice = McuModels.Device.objects.get(id=id)
	except: return redirect('web_mybox')
	if adevice.user != request.user: return redirect('web_mybox')
	# Action : Start
	if adevice.start_date != None: 
		adevice.start_date = None
		statusSet = adevice.state_set.filter(isEnable=True)
		for aStatus in statusSet:
			aStatus.isEnable = False
			aStatus.save()
	# Action : Stop
	else: 
		adevice.start_date = timezone.now()
	adevice.save()
	return redirect('/device/view/'+str(id)+'/')