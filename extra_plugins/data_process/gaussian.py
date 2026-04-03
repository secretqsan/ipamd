import copy
from scipy.ndimage import gaussian_filter

def func(data):
    res = copy.deepcopy(data)
    res.data = gaussian_filter(res, sigma=2, mode='reflect', truncate=3.0)