import copy
from functools import singledispatch
from ipamd.public.models.data import *
import numpy as np

@singledispatch
def func(data: Ratio, **kargs):
    sum = np.sum(data.data)
    normalized_data = data.data / sum
    res = copy.deepcopy(data)
    res.data = normalized_data
    if 'title' in kargs:
        res.meta['title'] = kargs['title']
    else:
        res.meta['title'] = data.meta['title'] + ' normalized'
    return res

@func.register(Vector)
@func.register(Matrix)
def _(data, **kargs):
    min_value = np.min(data.data)
    max_value = np.max(data.data)
    normalized_data = (data.data - min_value) / (max_value - min_value)
    res = copy.deepcopy(data)
    res.data = normalized_data
    if 'title' in kargs:
        res.meta['title'] = kargs['title']
    else:
        res.meta['title'] = data.meta['title'] + ' normalized'
    return res

@func.register
def _(data: PointSet,  **kargs):
    if 'target' not in kargs:
        normalize_x = True
        normalize_y = True
    else:
        normalize_x = 'x' in kargs['target']
        normalize_y = 'y' in kargs['target']
    res = copy.deepcopy(data)
    if normalize_x:
        x_data = data.data[:, 0]
        min_value = np.min(x_data)
        max_value = np.max(x_data)
        x_data = (x_data - min_value) / (max_value - min_value)
        res.data[:, 0] = x_data
    if normalize_y:
        y_data = data.data[:, 1]
        min_value = np.min(y_data)
        max_value = np.max(y_data)
        y_data = (y_data - min_value) / (max_value - min_value)
        res.data[:, 1] = y_data
    if 'title' in kargs:
        res.meta['title'] = kargs['title']
    else:
        res.meta['title'] = data.meta['title'] + ' normalized'
    return res

