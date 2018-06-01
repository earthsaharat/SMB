from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [

	path('',                                views.admin_home,           name='admin_home'),
	path('error/',                          views.admin_error,          name='admin_error'),

	path('order/',                          views.admin_order,          name='admin_order'),

	path('profile/',                        views.admin_profile,        name='admin_profile'),
	path('profile/add/',                    views.admin_profile_add,    name='admin_profile_add'),
	path('profile/edit/<int:id>/',          views.admin_profile_edit,   name='admin_profile_edit'),

	path('device/',                         views.admin_device,         name='admin_device'),
	path('device/edit/<int:id>/',           views.admin_device_edit,    name='admin_device_edit'),
	path('device/remove/<int:id>/',         views.admin_device_remove,  name='admin_device_remove'),
	# path('buybox/',                       views.buy_box,          name='buy_box'),
	# path('contact/',                      views.web_contact,      name='web_contact'),
	# path('product/',                      views.web_product,      name='web_product'),
	# path('product/addremove/<int:itemid>',    views.web_add_remove,   name='web_add_remove'),
	# path('device/all/',                   views.web_mybox,        name='web_mybox'),

]