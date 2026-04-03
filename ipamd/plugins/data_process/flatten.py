from ipamd.public.models.data import *
from functools import singledispatch
import numpy as np

@singledispatch
def func(data:Vector, by='average', **kargs):
    res_value = np.sum(data.data) if by != 'average' else np.average(data.data)
    return Scalar(
        title=kargs.get('title', data.meta['title'] + ' flattened'),
        data=res_value,
        unit=kargs.get('unit', '')
    )

@func.register
def _(data:Matrix, by='average', **kargs):
    res_value = (
        np.sum(data.data, axis=kargs['axis'])) if by != 'average' else np.average(data.data, axis=kargs['axis'])
    return Vector(
        title=kargs.get('title', data.meta['title'] + ' flattened'),
        data=res_value,
        x_axis=kargs.get('x_axis', data.meta['x_axis'] if kargs['axis']==0 else data.meta['y_axis']),
        x_label=kargs.get('x_label', data.meta['x_label'] if kargs['axis']==0 else data.meta['y_label']),
        y_label=kargs.get('y_label', data.meta['y_label'] if kargs['axis']==1 else data.meta['x_label']),
    )
