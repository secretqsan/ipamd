from ipamd import App
from ipamd.public.models.md import Unit
app = App('example', gpu_id=0).use('Calvados3')
app.gen_link()
app.load_file('fus.pdb')
mol = app.builder.protein_from_pdb('fus.pdb')
box = app.builder.new_simulation_box(20, 20, 100).in_solvent('pure water')
box.place_molecule_periodically(mol, 1, 1, 1)
simulation = app.simulation.new_simulation(
    box,
    'simulation',
    total_time=1 * Unit.TimeScale.ns,
    snap_shot=5
)
simulation.run()

density = app.mdanalysis.density_align(box=box, target_frame=0, d=5, direction='Z')
density_avg = app.mdanalysis.batch_compute('density_align', target_frame='1-3', box=box, d=5)
app.data_process.plot(density, appearance='heatmap')
app.data_process.plot(density_avg, appearance='heatmap')