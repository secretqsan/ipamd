from ipamd import App
from ipamd.public.models.md import Unit
app = App('example', gpu_id=7).use('slab_prepare')
app.gen_link()
app.load_file('fus.pdb')
box = app.builder.new_simulation_box(50, 50, 50).in_solvent('pure water')
mol = app.builder.protein_from_pdb('fus.pdb', rigid_range='285-371')
box.place_molecule_randomly(mol, 20, strict=True, allow_out_of_box=False)
simulation = app.simulation.new_simulation(box, 'slab_prepare', total_time=10*Unit.TimeScale.ns, snap_shot=10)
simulation.run()
