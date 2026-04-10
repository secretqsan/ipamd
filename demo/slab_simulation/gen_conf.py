from ipamd import App
from ipamd.public.models.md import Unit
from ipamd.public.models.sequence import ProteinSequence
app = App('example')
app.gen_link()
app.use('slab_prepare')
box = app.builder.new_simulation_box(20, 20, 60).in_solvent('pure water')
seq = ProteinSequence('test', 'F' * 50)
mol = app.builder.spiral_protein(seq)
box.place_molecule_randomly(mol, 80, strict=True)
simulation = app.simulation.new_simulation(box, 'simulation', total_time=10*Unit.TimeScale.ns, snap_shot=10)
simulation.run()