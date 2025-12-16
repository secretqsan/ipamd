from ipamd import App
from ipamd.public.models.md import Unit
# In this script we will generate an initial configuration with small amount of condensates
app = App('test').use('Initial')
box = app.builder.new_simulation_box(25, 25, 25).in_solvent('pure water')
mol = app.builder.molecule_from_xml('init_fus')
box.place_molecule_randomly(mol, 10, strict=True)
simulation = app.simulation.new_simulation(
    box,
    'init_condensate',
    total_time=50 * Unit.TimeScale.ns,
    snap_shot=10,
)
simulation.run()
box.to_xml('init_condensate')