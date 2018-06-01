from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [

    # path('', 			views.home, 														name='home'),
    path('login/', 		auth_views.login, 		{'template_name': 'auth_login.html'}, 		name='login'),
    path('logout/', 	auth_views.logout,		{'next_page': 'login'}, 					name='logout'),
    path('signup/', 	views.signup, 														name='signup'),
    path('password/', 	views.change_password, 												name='change_password'),

    path('info/', 		views.information, 		name='information'),

]