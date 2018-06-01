from django.contrib import admin

from . import models

# MARK : Action
def make_Enable(modeladmin, request, queryset):
    queryset.update(isEnable=True)
make_Enable.short_description = "Enable"

def make_Disable(modeladmin, request, queryset):
    queryset.update(isEnable=False)
make_Disable.short_description = "Disable"

# MARK : Model
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','isEnable','name','creator','create_date','lenDateStr','usingDeviceCount','image']
    actions = [make_Enable,make_Disable]
admin.site.register(models.Profile,ProfileAdmin)

class InstructionAdmin(admin.ModelAdmin):
    list_display = ['id','isEnable','profile','day','hour','temp','humi','r','g','b']
    actions = [make_Enable,make_Disable]
admin.site.register(models.Instruction,InstructionAdmin)

class DeviceAdmin(admin.ModelAdmin):
    list_display = ['id','isEnable','serial','user','profile','start_date']
    actions = [make_Enable,make_Disable]
admin.site.register(models.Device,DeviceAdmin)

class StateAdmin(admin.ModelAdmin):
    list_display = ['id','isEnable','device','date','temp','humi']
    actions = [make_Enable,make_Disable]
admin.site.register(models.State,StateAdmin)