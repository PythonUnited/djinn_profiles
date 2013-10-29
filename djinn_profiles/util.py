#-*- coding: utf-8 -*-
import sys
from django.conf import settings
from django.core import exceptions
from django.utils.importlib import import_module


def load_class(class_spec):

    parts = class_spec.split(".")

    module = __import__(".".join(parts[:-1]))

    import pdb; pdb.set_trace()
    
