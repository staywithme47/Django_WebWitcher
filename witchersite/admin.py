from django.contrib import admin
from . models import StartData, Action, Enemies, WitcherModel, DrownerModel, BanditModel, GhostModel
from . models import ModelGame
# Register your models here.

admin.site.register(StartData)
admin.site.register(Action)
admin.site.register(WitcherModel)
admin.site.register(DrownerModel)
admin.site.register(BanditModel)
admin.site.register(GhostModel)
admin.site.register(ModelGame)
