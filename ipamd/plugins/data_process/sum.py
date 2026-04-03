from ipamd.public.utils.output import error
from ipamd.public.models.data import *
import copy

def func(data, *args: Scalar):
    if isinstance(data, Series):
        error('Cannot compute the average value of a group of points')
        return

    res = copy.deepcopy(data)
    sum_data = res.data
    for scalar in args:
        sum_data += scalar.data
    res.update(sum_data / (len(args) + sum_data))
    return res