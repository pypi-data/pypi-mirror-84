#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Model definitions and handling
"""
from .model import Model, ModelFixed, ModelSelect, ModelWeighted
from .model import ModelInterpolate
from .model import model_from_dict
from .fitter import fit_mock, fit_optimize, fit_select, fit_interpolate
