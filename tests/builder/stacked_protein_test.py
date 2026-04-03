from ipamd import App
from ipamd.public.models.md import Unit
app = App('example', gpu_id=0).use('Calvados3')
app.gen_link()
app.load_file('fus.pdb')
mol = app.builder.protein_from_pdb('fus.pdb')
box = app.builder.new_simulation_box(20, 20, 50).in_solvent('pure water')
box.place_molecule_periodically(mol, 1, 1, 1)
simulation = app.simulation.new_simulation(
    box,
    'simulation',
    total_time=2 * Unit.TimeScale.ns,
    snap_shot=20
)
simulation.run()
app.data_process.plot(
    app.mdanalysis.batch_compute('density_align', box=box, target_frame='1-5', d=0.2)
)
app.data_process.print(
    app.mdanalysis.slab_free_energy(box=box, target_frame='10-20', d=0.2)
)