from ipamd import App
from ipamd.public.models.md import Environment
from ipamd.public.utils.monitor import monitor_time

app = App('computation_efficiency', gpu_id=1).use('Calvados1')
app.load_file('input_data/fus.pdb')
mol = app.builder.protein_from_pdb('fus.pdb', rigid_from_plddt=True)
box = app.builder.new_simulation_box(150, 150, 150)
env = Environment('normal saline')
box.in_solvent(env)
#box.place_molecule_randomly(mol, 512, max_tries=50)
simulation = app.simulation.new_simulation(box, 'fus512', total_time='500ns', snap_shot=50)
@monitor_time
def run():
    simulation.run()
    return 0
_, time = run()
print(f'Running time: {time} seconds')
