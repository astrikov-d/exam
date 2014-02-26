# -*- coding: utf-8 -*-
__author__ = 'Dmitry Astrikov'

from django import forms

from models import Models


class UsersForm(forms.ModelForm):
    class Meta:
        model = Models.get_model('Users')

class RoomsForm(forms.ModelForm):
    class Meta:
        model = Models.get_model('Rooms')
