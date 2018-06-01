from django.urls import path
from . import views

urlpatterns = [

    # path('', 								views.home, 			name='home'),
    # path('buybox/', 						views.buy_box, 			name='buy_box'),
    # path('contact/', 						views.web_contact, 		name='web_contact'),
    # path('product/', 						views.web_product, 		name='web_product'),
    # path('product/addremove/<int:itemid>',	views.web_add_remove,	name='web_add_remove'),
    # path('device/all/', 					views.web_mybox, 		name='web_mybox'),

    path('', 								views.handleUpdate, 	name='mcu_handle_update'),
]