from ipamd import App
app = App('fusattr', gpu_id=2)
box1 = app.builder.new_simulation_box(50, 50, 50)
box1.in_solvent('pure water')
app.load_file('fus.pdb')
mol1 = app.builder.protein_from_pdb('fus.pdb', rigid_from_plddt=True)
box1.place_molecule_randomly(mol1, 10, max_tries=10)
simulation = app.simulation.new_simulation(box1, 'simulation', total_time=100, snap_shot=20)
simulation.run()

rg = box1.compute(app.analysis.rg, 'Rg')
rg_distro = rg.distribution(bins=7)
rg_distro.plot(style = {
    'y_label': 'n',
    'x_label': 'Rg (nm)',
    'title': '',
    'size': [4.75, 4.7]
}, save=True)
cm = box1.compute(app.analysis.contact_map, 'ContactMap', type1='fus')
cm.plot(style = {
    'title': '',
    'x_label': 'residue index',
    'y_label': 'residue index'
}, save=True)
rmsf = box1.compute(app.analysis.rmsf, 'RMSF', target_frame='1-4')
rmsf.plot(style = {
    'title': '',
    'x_label': 'residue index',
    'y_label': 'RMSF (nm)',
    'color': 'Orange',
    'size': [4.8, 4.7]
}, save=True)
box1.frame(20)
ripley = box1.compute(app.analysis.ripley, 'Ripley', end_d=60, l=True)
ripley_ref = box1.compute(app.analysis.ripley, 'Ripley', end_d=60, ref=True, l=True)
box1.frame(1)
ripley1 = box1.compute(app.analysis.ripley, 'Ripley', end_d=60, l=True)
ripley1.plot(style = {
    'x_label': 'r (nm)',
    'y_label': 'Ripley L (nm)',
    'title': '',
    'size': [4.7, 4.7],
    'legend': [
        "Ripley's L",
        'L=0'
    ]
}, ref=[
    ripley_ref
], save=True)