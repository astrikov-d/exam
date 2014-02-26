# -*- coding: utf-8 -*-
__author__ = 'Dmitry Astrikov'

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseBadRequest

from models import Models


class IndexView(View):
    def get(self, request, *args, **kwargs):
        Users = Models.get_model('Users')
        #Rooms = Models.get_model('Rooms')

        return render(request, "app/index.html", {
            'users': Users.objects.all()
        })

    def post(self, request, *args, **kwargs):
        if 'model_name' not in request.POST or 'field_name' not in request.POST or 'value' not in request.POST:
            return HttpResponseBadRequest()
        else:
            Model = None