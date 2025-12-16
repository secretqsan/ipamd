from ipamd import App
from ipamd.public.models.md import Environment, Unit

app = App(name = 'hpst').use('HPST')
box = app.builder.new_simulation_box(50, 50, 50)
env = Environment('normal saline')
env.set_temperature(323)
box.in_solvent(env)
mol = app.builder.spiral_protein('elp', 'VPGMG' * 80)
box.place_molecule_randomly(mol, 100, max_tries=15)
simulation = app.simulation.new_simulation(box, 'simulation', total_time=10 * Unit.TimeScale.ns, snap_shot=20, thermo_bath='npt_z')
simulation.run()