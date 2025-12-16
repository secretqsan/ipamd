from ipamd import App
app = App('fusattr', gpu_id=2)
box = app.builder.new_simulation_box(50, 50, 50)
box.in_solvent('pure water')
app.builder.download_pdb('1aki')
mol1 = app.builder.protein_from_pdb('1aki.pdb', rigid_from_plddt=True)
box.place_molecule_randomly(mol1, 30, max_tries=10, allow_out_of_box=False)

ripley = box.compute(app.analysis.ripley, 'Ripley', end_d=60, l=True)
ripley_ref = box.compute(app.analysis.ripley, 'Ripley', end_d=60, l=True, ref=True)
box.to_xml('ripley_l')
ripley.plot(style = {
    'x_label': 'r (nm)',
    'y_label': 'Ripley L (nm)',
    'title': '',
    'size': [5.2, 4.7],
    'legend': [
        'ripley L',
        'y=0'
    ]
},
ref = [ripley_ref]
)