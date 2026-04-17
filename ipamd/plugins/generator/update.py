"""update the force field of the molecule"""
configure = {
    "apply": ['ff']
}
def func(molecule, ff):
    """plugin main function"""
    for atom in molecule.atoms:
        atom['prototype'].update(ff)
