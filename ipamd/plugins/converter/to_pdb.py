import os.path
from pypdbio import PdbWriter, Model, Chain, Residue, Atom
from pybioseq.converter import to3
from ipamd.public.utils.output import warning

configure = {
    "schema": 'frame',
    "apply": ['persistency_dir']
}

def func(filename, persistency_dir, frame, ignoring_pbc = True, atom_type_override=''):
    prop = frame.properties(ignoring_image=ignoring_pbc)
    molecules = prop['molecules']
    n_molecules = len(molecules)
    if n_molecules >= 26:
        warning('Chain number exceeds the limit of pdb file. Use cif instead.')

    writer = PdbWriter(
        os.path.join(persistency_dir, filename + '.pdb')
    )

    model = Model()
    for molecule in enumerate(molecules):
        chain = Chain()
        for i, type_ in enumerate(molecule['type']):
            residue = Residue(to3(type_).upper())
            residue.add_atom(Atom(
                typ="ATOM",
                name=type_ if atom_type_override == '' else atom_type_override,
                coord=molecule['position'][i],
                element='C'
            ))
            chain.add_residue(residue)
        model.add_chain(chain)

        n_total += len(molecule['type'])
    writer.write(model)
