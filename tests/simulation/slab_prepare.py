from ipamd import App
from ipamd.public.models.md import Unit
app = App('example', gpu_id=2).use('slab_prepare')
app.load_file('fus.pdb')
box = app.builder.new_simulation_box(40, 40, 40).in_solvent('pure water')
mol = app.builder.protein_from_pdb('fus.pdb', rigid_range='285-371')
box.place_molecule_randomly(mol, 20, strict=True)
simulation = app.simulation.new_simulation(box, 'simulation', total_time=100*Unit.TimeScale.ns, snap_shot=10)
simulation.run()
