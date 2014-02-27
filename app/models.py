# -*- coding: utf-8 -*-
__author__ = 'Dmitry Astrikov'

import yaml

from django.db import models
from django.conf import settings


class DynamicModel(object):
    created_models = {}

    def __init__(self, file_path):
        """
        Class constructor, read YAML data and create models from it.
        """

        stream = open(settings.PROJECT_ROOT + file_path, "r")

        yaml_contents = yaml.load(stream)

        for model in yaml_contents:
            meta = type('Meta', (), {
                "verbose_name": yaml_contents[model]['title'],
                "verbose_name_plural": yaml_contents[model]['title']
            })
            model_attributes = {
                '__module__': __name__,
                'Meta': meta
            }
            for field in yaml_contents[model]['fields']:
                model_attributes.update({field['id']: self.get_model_field(field['type'], field['title'])})
            model_object = type(model.capitalize(), (models.Model,), model_attributes)

            setattr(model_object, 'app_label', __name__.split('.')[-2])

            self.created_models.update({model.capitalize(): model_object})

    def get_model(self, model_name):
        """
        Try to return created model.
        """

        try:
            return self.created_models[model_name]
        except KeyError:
            return None

    def get_created_models(self):
        """
        Return availavle models.
        """

        return self.created_models

    def get_model_field(self, field_type, field_title):
        """
        Simple model fields dict.
        """

        fields = {
            'char': models.CharField(max_length=32, verbose_name=field_title),
            'int': models.IntegerField(verbose_name=field_title),
            'date': models.DateField(verbose_name=field_title)
        }
        try:
            return fields[field_type]
        except KeyError:
            return fields['char']


Models = DynamicModel(settings.PROJECT_ROOT + '/app/conf/models.yaml')