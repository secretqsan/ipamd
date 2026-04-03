"""
plugin for calculating density along a axis
"""
import math
import numpy as np
from ipamd.public.models.data import Vector
from ipamd.public.utils.parser import protein_range_split
from ipamd.public.constant import na

configure = {
    "schema": ['frame'],
}

def func(frame, target_molecule=None, direction='Z', d=1, **kwargs):
    """
    main function for calculating density along a axis

    :param target_molecule: the target molecule to calculate. If None, calculate for all molecules.
    :param direction: the direction of the simulation
    :param d: bin size
    :param kwargs: other parameters, don't need to be set

    :return: a vector containing the density along the axis
    """
    prop = frame.properties(ignoring_image=False)
    box_size = prop['size']
    molecules = prop['molecules']

    if direction.upper() == 'X':
        idx = 0
    elif direction.upper() == 'Y':
        idx = 1
    else:
        idx = 2

    length = box_size[idx]
    mass_list = np.zeros(math.ceil(length / d))
    pos_list = []
    width_list = []
    pos_start = -length / 2
    while len(pos_list) < math.ceil(length / d):
        distance_to_end = length / 2 - pos_start
        if distance_to_end >= d and len(pos_list) < math.ceil(length / d) - 1:
            pos_list.append(pos_start + d / 2)
            width_list.append(d)
        else:
            pos_list.append(pos_start + distance_to_end / 2)
            width_list.append(distance_to_end)
        pos_start += d

    area = box_size[0] * box_size[1] * box_size[2] / box_size[idx]
    volume_list = np.array(width_list) * area

    target_molecule_type, target_range = protein_range_split(target_molecule)
    for molecule in molecules:
        molecule_type = molecule['molecule_type']
        if target_molecule_type != "" and molecule_type != target_molecule_type:
            continue
        position = molecule['position']
        mass = molecule['mass']
        molecule_length = len(mass)
        for i in range(molecule_length):
            if target_range != [] and i not in target_range:
                continue
            index = int((position[i][idx] + length / 2) / d)
            if 0 <= index < len(mass_list):
                mass_list[index] += mass[i]
            elif index == len(mass_list):
                mass_list[index - 1] += mass[i]

    density_list = mass_list / volume_list / 1000 / na * 1e24

    return Vector(
        data=density_list,
        title=f'Density along {direction.upper()} axis',
        y_label='Density (g/mL)',
        x_label='Position (nm)',
        x_axis=pos_list
    )
