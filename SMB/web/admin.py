from django.contrib import admin

from . import models

class GroupItemAdmin(admin.ModelAdmin):
    list_display = ('id','name','image')
admin.site.register(models.GroupItem,GroupItemAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id','name','group','cost')
admin.site.register(models.Item,ItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','date','address','items','status')
admin.site.register(models.Order,OrderAdmin)