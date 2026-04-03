from ipamd.public.models.data import *

scalar = Scalar(
    title='data',
    data=12.34,
    unit='m/s'
)

vector = Vector(
    title='vector',
    data=[1.0, 2.0, 3.0],
)
point_set = PointSet(
    title='Temperature Over Time',
    data=[[0, 22.5], [1, 23.0], [2, 21.5], [3, 24.0]],
    x_label='Time (hours)',
    y_label='Temperature (°C)',
)
matrix = Matrix(
    'Contact Map',
    [[1, 2, 3], [4, 5, 6]],
    "Amino Acids",
    "Amino Acids",
)
ratio = Ratio(
    title='Success Rate',
    data=[75, 2, 1],
    labels=['Success', 'Failure', 'None'],
)
distribution = Distribution(
    title='Height Distribution',
    data=[1, 3, 5],
    bins=2,
)