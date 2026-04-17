from ipamd import App
from ipamd.public.models.md import Unit
app = App('test', gpu_id=7).use('Calvados3')

box = app.builder.new_simulation_box(50, 50, 50).in_solvent('pure water')

simulation = app.simulation.new_simulation(
    box,
    'fixed_particles_test',
    total_time=1 * Unit.TimeScale.ns,
    snap_shot=10,
    fixed_particle=list(range(500))
)
app.gen_link()
app.load_file('fus.pdb')
mol = app.builder.protein_from_pdb('fus.pdb')
box.place_molecule_randomly(mol, 10)
simulation.run("y")
