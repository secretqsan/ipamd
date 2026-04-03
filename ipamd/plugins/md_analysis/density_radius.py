"""
plugin for calculating density in a radius
"""
import math
import numpy as np
from ipamd.public.constant import na
from ipamd.public.models.data import Vector
from ipamd.public.utils.parser import protein_range_split
configure = {
    "schema": ['frame'],
}

def func(frame, cutoff, target_molecule="", origin=(0, 0, 0), d=1, **kwargs):
    prop = frame.properties(ignoring_image=False)
    box_size = prop['size']
    molecules = prop['molecules']
    origin_pos = np.array(origin)

    mass_list = np.zeros(math.ceil(cutoff / d))
    radius_list = []
    dr_list = []
    pos_start = 0
    while len(radius_list) < math.ceil(cutoff / d):
        distance_to_end = cutoff - pos_start
        if distance_to_end >= d and len(radius_list) < math.ceil(cutoff / d) - 1:
            # to avoid floating point error, append the last bin in the end
            radius_list.append(pos_start + d / 2)
            dr_list.append(d)
        else:
            radius_list.append(pos_start + distance_to_end / 2)
            dr_list.append(distance_to_end)
        pos_start += d
    radius_list = np.array(radius_list)
    dr_list = np.array(dr_list)
    volume_list = math.pi * 4 / 3 * \
        ((radius_list + dr_list / 2) ** 3 - (radius_list - dr_list / 2) ** 3)

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
            min_period_x = math.floor((origin_pos[0] - cutoff - position[i][0]) / box_size[0])
            min_period_y = math.floor((origin_pos[1] - cutoff - position[i][1]) / box_size[1])
            min_period_z = math.floor((origin_pos[2] - cutoff - position[i][2]) / box_size[2])
            max_period_x = math.ceil((origin_pos[0] + cutoff - position[i][0]) / box_size[0])
            max_period_y = math.ceil((origin_pos[1] + cutoff - position[i][1]) / box_size[1])
            max_period_z = math.ceil((origin_pos[2] + cutoff - position[i][2]) / box_size[2])
            for x in range(min_period_x, max_period_x + 1):
                for y in range(min_period_y, max_period_y + 1):
                    for z in range(min_period_z, max_period_z + 1):
                        mirrored_pos = np.array(
                            [x * box_size[0], y * box_size[1], z * box_size[2]]
                        ) + np.array(position[i])
                        distance = np.sqrt(np.sum((mirrored_pos - origin_pos) ** 2))
                        if distance > cutoff:
                            continue
                        index = int(distance / d)
                        mass_list[index] += mass[i]

    density_list = mass_list / volume_list / 1000 / na * 1e24

    return Vector(
        data=density_list,
        title=f'Density from origin {origin}',
        y_label='Density (g/mL)',
        x_label='Radius (nm)',
        x_axis=radius_list
    )
