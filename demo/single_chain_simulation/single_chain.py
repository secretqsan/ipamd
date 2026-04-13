from ipamd import App
from ipamd.public.models.md import Unit
app = App('example')
box = app.builder.new_simulation_box(20, 20, 20).in_solvent('pure water')
app.builder.load_example_molecule('fus')
mol = app.builder.protein_from_pdb('fus.pdb', rigid_from_plddt=True)
box.place_molecule_periodically(mol, 1, 1, 1)
simulation = app.simulation.new_simulation(
    box,
    'simulation',
    total_time=1*Unit.TimeScale.ns,
    snap_shot=10
)
simulation.run()
