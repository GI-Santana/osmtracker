from follower.mapper import Mapper
from follower.models import Email
from follower.reachout import ReachOut
from django.contrib import admin


class EmailAdmin(admin.ModelAdmin):
    list_display = ['subject']

admin.site.register(Email,EmailAdmin)

class ReachOutInline(admin.TabularInline):
    model=Mapper.reach_outs.through
    can_delete=False
    extra=0
    can_delete=False

class MapperAdmin(admin.ModelAdmin):
    list_display=['user']
    inlines = [ ReachOutInline ]

admin.site.register(Mapper,MapperAdmin)

class ReachOutAdmin(admin.ModelAdmin):
    list_display=['mapper']

admin.site.register(ReachOut,ReachOutAdmin)
