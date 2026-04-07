import os
from shutil import copyfile
from ipamd.public.utils.output import error
from ipamd.public import shared_data
configure = {
    "schema": 'io',
}
def func(molecule_name, working_dir):
    mol_db_dir = os.path.join(shared_data.module_installation_dir, 'data/molecules')
    molecule_file_path = os.path.join(mol_db_dir, molecule_name + '.pdb')
    target_file_path = os.path.join(working_dir, molecule_name + '.pdb')
    if os.path.exists(molecule_file_path):
        copyfile(
            molecule_file_path,
            target_file_path
        )
    else:
        error(f"No molecule {molecule_name} file found.")
        return
