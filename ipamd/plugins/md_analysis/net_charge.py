import numpy as np
from numba import cuda
from ipamd.public.models.data import Matrix
configure = {
    "schema": ['frame'],
}
def func(frame, threshold=4, type1='', type2='', mode='', **kwargs):
    prop = frame.properties(ignoring_image=False)
    molecules = prop['molecules']
    box_size = prop['size']
    threshold_square = threshold ** 2
    if type1 == '':
        type1 = molecules[0]['molecule_type']
    if type2 == '':
        type2 = type1

    molecule_of_type1_list = []
    for molecule in molecules:
        if molecule['molecule_type'] == type1:
            molecule_of_type1_list.append(molecule)
    molecule_of_type2_list = []
    for molecule in molecules:
        if molecule['molecule_type'] == type2:
            molecule_of_type2_list.append(molecule)

    molecule_length_type1 = len(molecule_of_type1_list[0]['mass'])
    molecule_length_type2 = len(molecule_of_type2_list[0]['mass'])

    position_list_1 = []
    position_list_2 = []
    for molecule in molecule_of_type1_list:
        for pos in molecule['position']:
            position_list_1.append(pos)
    for molecule in molecule_of_type2_list:
        for pos in molecule['position']:
            position_list_2.append(pos)
    position_list_1 = np.array(position_list_1, dtype=np.float32)
    position_list_2 = np.array(position_list_2, dtype=np.float32)
    origin_pos_list_device = cuda.to_device(position_list_1)
    target_pos_list_device = cuda.to_device(position_list_2)

    box_size_device = cuda.to_device(np.array(box_size, dtype=np.float32))

    contact_map = np.zeros((molecule_length_type1, molecule_length_type2), dtype=np.int32)
    contact_map_device = cuda.to_device(contact_map)

    @cuda.jit
    def compute_contacts(
            target_pos_list,
            origin_pos_list,
            molecule_length_1,
            molecule_length_2,
            box_size,
            exclude_mode,
            res_matrix
    ):
        thread_index = cuda.grid(1)
        i = thread_index
        while i < len(target_pos_list):
            position_1 = target_pos_list[i]
            for j in range(len(origin_pos_list)):
                molecule_index_1, residue_index_1 = divmod(i, molecule_length_1)
                molecule_index_2, residue_index_2 = divmod(j, molecule_length_2)

                position_2 = origin_pos_list[j]
                dx = abs(position_1[0] - position_2[0])
                dy = abs(position_1[1] - position_2[1])
                dz = abs(position_1[2] - position_2[2])

                if dx > box_size[0] / 2:
                    dx = box_size[0] - dx
                if dy > box_size[1] / 2:
                    dy = box_size[1] - dy
                if dz > box_size[2] / 2:
                    dz = box_size[2] - dz

                distance_square = dx * dx + dy * dy + dz * dz
                if exclude_mode == 1 and i == j:
                    continue
                if exclude_mode == 2 and molecule_index_1 == molecule_index_2:
                    continue
                if exclude_mode == 3 and molecule_index_1 != molecule_index_2:
                    continue
                if distance_square < threshold_square:
                    cuda.atomic.add(res_matrix, (residue_index_1, residue_index_2), 1)
            i += cuda.gridsize(1)

    exclude_mode = 0
    if type1 == type2:
        if mode == '':
            exclude_mode = 1
        elif mode == 'inter':
            exclude_mode = 2
        elif mode == 'intra':
            exclude_mode = 3

    compute_contacts[1024, 128](
        target_pos_list_device,
        origin_pos_list_device,
        molecule_length_type1,
        molecule_length_type2,
        box_size_device,
        exclude_mode,
        contact_map_device
    )
    contact_map = contact_map_device.copy_to_host()

    return Matrix(
        data=contact_map,
        title='Contact Map',
        x_label=f'Amino Acid Index of {type2}',
        y_label=f'Amino Acid Index of {type1}',
    )