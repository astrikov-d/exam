# -*- coding: utf-8 -*-
__author__ = 'Dmitry Astrikov'

from django import forms

from models import Models


class DynamicModelForm():
    form_object = None

    def __init__(self, model):
        model = Models.get_model(model)
        meta = type('Meta', (), {"model": model, })
        self.form_object = type('DynamicModelForm', (forms.ModelForm,), {"Meta": meta})

    def get_form(self):
        return self.form_object

