from ipamd import App
from ipamd.public.models.md import Unit
app = App('test', gpu_id=1).use('Calvados3')

box = app.builder.new_simulation_box(50, 50, 50).in_solvent('pure water')

simulation = app.simulation.new_simulation(
    box,
    'simulation',
    total_time=10 * Unit.TimeScale.ns,
    snap_shot=10
)
if not simulation.exist():
    app.gen_link()
    app.load_file('fus.pdb')
    mol = app.builder.protein_from_pdb('fus.pdb')
    box.place_molecule_randomly(mol, 10)
simulation.run("n")
app.data_process.plot(
    app.mdanalysis.batch_compute(
        'density_radius', box=box, cutoff=50, target_molecule='fus@all', target_frame='1-10', d=1
    ),
    save_figure=True
)
