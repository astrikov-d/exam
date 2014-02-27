# -*- coding: utf-8 -*-
__author__ = 'Dmitry Astrikov'

import json
import datetime


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return datetime.datetime.strftime(obj, "%Y-%m-%d")

        return json.JSONEncoder.default(self, obj)
