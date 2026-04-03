from ipamd import App
from ipamd.public.models.sequence import ProteinSequence
app = App('example', gpu_id=7).use('Calvados3')
app.gen_link()
prot = ProteinSequence('name', 'GGGGG' * 100)
mol = app.builder.stacked_protein(prot)
box = app.builder.new_simulation_box(20, 20, 20).in_solvent('pure water')
box.place_molecule_periodically(mol, 1, 1, 1)
simulation = app.simulation.new_simulation(box, 'stacked_protein_test', total_time=1000, snap_shot=4)
simulation.run()