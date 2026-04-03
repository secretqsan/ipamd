from ipamd.public.models.data import *
import copy
import numpy as np

def func(data, **kargs):
    res = copy.deepcopy(data)
    res.data = np.