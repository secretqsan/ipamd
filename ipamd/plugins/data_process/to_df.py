import pandas as pd
from ipamd.public.models.data import *
from functools import singledispatch

def func(data):
    data = convert(data)
    return pd.DataFrame(data)

@singledispatch
def convert(data):
    raise NotImplementedError(f'Output for data type {type(data)} is not implemented.')

@convert.register
def _(data: Scalar):
    return {'Value': [data.data.item()]}

@convert.register
def _(data: Vector):
    res = {}
    for key, value in zip(data.meta['x_axis'], data.data):
        res[key] = [value.item()]
    return res

@convert.register
def _(data: PointSet):
    x_label = data.meta['x_label']
    y_label = data.meta['y_label']
    res = {
        x_label: [],
        y_label: []
    }
    for vector in data.data:
        res[x_label].append(vector[0].item())
        res[y_label].append(vector[1].item())
    return res

@convert.register
def _(data: Matrix):
    res = {}
    for idx, x_val in enumerate(data.meta['x_axis']):
        res[x_val] = []
        for vector in data.data:
            res[x_val].append(vector[idx].item())
    return res

@convert.register
def _(data: Ratio):
    res = {}
    for key, value in zip(data.meta['labels'], data.data):
        res[key] = [value.item()]
    return res

@convert.register
def _(data: Distribution):
    return {
        data.meta['label']: data.data
    }
