# -*- coding: utf-8 -*-
__author__ = 'Dmitry Astrikov'

from django.contrib import admin

from models import Models


class UsersAdmin(admin.ModelAdmin):
    pass


admin.site.register(Models.get_model('Users'), UsersAdmin)


class RoomsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Models.get_model('Rooms'), RoomsAdmin)