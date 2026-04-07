def func(molecule):
    for atom in molecule.atoms:
        rigid_group = atom['rigid_group']
        if rigid_group >= 0:
            atom_type = atom["prototype"].get("type")
            if atom_type[-1] != "0":
                atom_type = f"{atom_type}0"
                atom["prototype"].set("type", atom_type)

    return molecule
