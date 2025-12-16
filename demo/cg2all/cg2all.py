from ipamd import App
from ipamd.public.models.md import Environment, Unit

app = App(name = 'cg2all', gpu_id=6)
box = app.builder.new_simulation_box(20, 20, 20)
env = Environment('normal saline')
box.in_solvent(env)
seq = app.sakuanna.new_protein_sequence(name='elp', sequence='VPGMG' * 60)
mol = app.builder.spiral_protein(seq)
box.place_molecule_randomly(mol, 5, max_tries=15)
simulation = app.simulation.new_simulation(box, 'simulation', total_time=1 * Unit.TimeScale.ns, snap_shot=4, thermo_bath='npt_z')
simulation.run()
box.to_aa('aa')