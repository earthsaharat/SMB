from django.contrib import admin

from . import models

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','user','lineid','facebook','phone','address')
admin.site.register(models.Customer,CustomerAdmin)