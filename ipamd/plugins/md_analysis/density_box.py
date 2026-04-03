from ipamd.public.constant import na
from ipamd.public.models.data import Scalar
configure = {
    "schema": ['frame'],
}

def func(frame, x0=0, y0=0, z0=0, lx=0, ly=0, lz=0, **kwargs):
    prop = frame.properties(ignoring_image=False)
    box_size = prop['size']
    molecules = prop['molecules']

    if lx == 0:
        lx = box_size[0]
    if ly == 0:
        ly = box_size[1]
    if lz == 0:
        lz = box_size[2]
    volume = lx * ly * lz

    mass_in_box = 0
    for molecule in molecules:
        position = molecule['position']
        mass = molecule['mass']
        molecule_length = len(mass)
        for i in range(molecule_length):
            if (position[i][0] > x0 and position[i][0] < x0 + lx and
                position[i][1] > y0 and position[i][1] < y0 + ly and
                position[i][2] > z0 and position[i][2] < z0 + lz):
                mass_in_box += mass[i]

    if volume == 0:
        density = 0
    else:
        density = mass_in_box / volume / 1000 / na * 1e24

    return Scalar(
        title='density',
        data=density,
        unit='g/cm3'
    )
