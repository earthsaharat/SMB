from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [

	path('', 								views.home, 			name='home'),
	path('buybox/', 						views.buy_box, 			name='buy_box'),

	path('profile/', 						views.web_profile, 		name='web_profile'),
	path('contact/', 						views.web_contact, 		name='web_contact'),

	path('order/',							views.web_order,		name='web_order'),
	path('order/confirm/',					views.web_order_confirm,name='web_order_confirm'),
	path('order/add/',						views.web_order_add,	name='web_order_add'),
	path('order/payment/',					views.web_order_payment,name='web_order_payment'),

	path('product/',						views.web_product,		name='web_product'),
	path('product/addremove/<int:itemid>/',	views.web_add_remove,	name='web_add_remove'),

	path('device/', 						views.web_mybox, 		name='web_mybox'),
	path('device/view/<int:id>/', 			views.web_mybox_view, 	name='web_mybox_view'),
	path('device/edit/<int:id>/', 			views.web_mybox_edit, 	name='web_mybox_edit'),
	path('device/action/<int:id>/', 		views.web_mybox_action, name='web_mybox_action'),

]