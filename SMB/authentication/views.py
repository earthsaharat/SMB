from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,update_session_auth_hash

from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm

from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse

from . import models

def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			models.Customer.objects.create(user=user)
			return redirect('information')
	else:
		form = UserCreationForm()
	return render(request, 'auth_register.html', {'form': form})

def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return redirect('home')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'auth_change_password.html', {
		'form': form
	})


@login_required
def information(request):
	try:
		aCustomer = models.Customer.objects.get(user=request.user)
	except:
		aCustomer = models.Customer.objects.create(user=request.user)
	if request.method == 'POST':
		request.user.first_name = request.POST['firstname']
		request.user.last_name  = request.POST['lastname']
		request.user.email      = request.POST['email']
		request.user.save()
		aCustomer.phone     = request.POST['phone']
		aCustomer.lineid    = request.POST['lineid']
		aCustomer.facebook  = request.POST['facebook']
		aCustomer.address   = request.POST['address']
		aCustomer.save()
		return redirect('home')
	return render(request,'auth_information.html',{
			'phone'     : aCustomer.phone 		if aCustomer.phone 		!= None else "",
			'lineid'    : aCustomer.lineid 		if aCustomer.lineid 	!= None else "",
			'facebook'  : aCustomer.facebook 	if aCustomer.facebook 	!= None else "",
			'address'   : aCustomer.address 	if aCustomer.address 	!= None else "",
		})