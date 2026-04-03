configure = {
    "apply": ['ff']
}
def func(molecule, ff):
    for atom in molecule.atoms:
        atom['prototype'].update(ff)