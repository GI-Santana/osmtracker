from follower.mapper import Mapper
from follower.models import Email
from django.contrib import admin


class EmailAdmin(admin.ModelAdmin):
    list_display = ['subject']

admin.site.register(Email,EmailAdmin)

class MapperAdmin(admin.ModelAdmin):
    list_display=['user']
admin.site.register(Mapper,MapperAdmin)

