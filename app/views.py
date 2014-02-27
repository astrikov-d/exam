# -*- coding: utf-8 -*-
__author__ = 'Dmitry Astrikov'

import json, cgi

from django.shortcuts import render
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.http import HttpResponseBadRequest, Http404, HttpResponse
from django.template.loader import render_to_string
from django.forms import ValidationError

from utils import DateTimeEncoder
from models import Models
from forms import DynamicModelForm


class IndexView(View):
    def get(self, request, *args, **kwargs):
        """
        Return initial template.
        """

        if request.is_ajax():
            model = Models.get_model(kwargs['model_name'])
            if not model:
                raise Http404
            fields = [f.name for f in model._meta.fields]
            qs = model.objects.all().order_by('id').values_list(*fields)
            fields = [f.verbose_name for f in model._meta.fields]
            form = DynamicModelForm(kwargs['model_name']).get_form()
            response = {'fields': fields, 'data': list(qs), 'form': render_to_string('app/form.html', {'form': form})}

            return HttpResponse(json.dumps(response, cls=DateTimeEncoder), mimetype='application/json')

        models = Models.get_created_models()
        return render(request, "app/index.html", {
            'models': models
        })

    def post(self, request, *args, **kwargs):
        """
        Changing the model field via table.
        """

        if 'model_name' not in request.POST or 'field_index' not in request.POST or 'model_pk' not in request.POST or 'value' not in request.POST:
            return HttpResponseBadRequest()
        else:
            try:
                model = Models.get_model(request.POST.get('model_name'))
                obj = model.objects.get(pk=request.POST.get('model_pk'))
                field = [f.name for f in model._meta.fields][int(request.POST.get('field_index'))]
                try:
                    setattr(obj, field, cgi.escape(request.POST.get('value')))
                    obj.full_clean()
                    obj.save()
                    response = {
                        'result': 'success'
                    }
                except ValidationError:
                    response = {
                        'result': 'error',
                        'error': u"Поле заполнено неправильно"
                    }
                return HttpResponse(json.dumps(response, cls=DateTimeEncoder), mimetype='application/json')
            except model.DoesNotExist:
                raise Http404


class MCreateView(CreateView):
    def post(self, request, *args, **kwargs):
        """
        Form submit.
        """

        if not request.is_ajax():
            return HttpResponseBadRequest
        model_name = request.POST.get('model_name', '')
        model = Models.get_model(model_name)
        if model is None:
            return HttpResponseBadRequest()
        form_class = DynamicModelForm(model_name).get_form()
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            response = {
                'result': 'success'
            }
        else:
            errors = {}
            for k in form.errors:
                errors[k] = form.errors[k][0]

            response = {
                'result': 'error',
                'errors': errors
            }
        return HttpResponse(json.dumps(response, cls=DateTimeEncoder), mimetype='application/json')