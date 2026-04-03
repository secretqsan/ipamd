from functools import singledispatch
from ipamd.public.models.data import *
from ipamd.public.utils.output import output, tabulate
import numpy as np
import csv

def func(data, filename):
    with open(filename, 'w') as file:
        csv_writer = csv.writer(file)
        write_data(data, csv_writer)

@singledispatch
def write_data(data, csv_writer):
    raise NotImplementedError(f'Output for data type {type(data)} is not implemented.')

@write_data.register
def _(data: Scalar, csv_writer):
    csv_writer.writerow([data.data.item()])

@write_data.register
def _(data: Vector, csv_writer):
    csv_writer.writerow(data.meta['x_axis'])
    csv_writer.writerow(data.data.tolist())

@write_data.register
def _(data: Series, csv_writer):
    csv_writer.writerow([data.meta['x_label'], data.meta['y_label']])
    for vector in data.data:
        csv_writer.writerow(vector.tolist())

@write_data.register
def _(data: Matrix, csv_writer):
    csv_writer.writerow(['', *data.meta['x_axis']])
    line_idx = 0
    for vector in data.data:
        csv_writer.writerow([data.meta['y_axis'][line_idx], *vector.tolist()])
        line_idx += 1

@write_data.register
def _(data: Ratio, csv_writer):
    csv_writer.writerow(data.meta['labels'])
    csv_writer.writerow(data.data.tolist())

@write_data.register
def _(data: Distribution, csv_writer):
    csv_writer.writerow([data.meta['label']])
    for value in data.data:
        csv_writer.writerow([value.item()])
