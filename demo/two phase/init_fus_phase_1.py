from ipamd import App
from ipamd.public.models.md import Unit
# In initial force field the particles are greatly attractive to each other
# this script can make a protein become very compact so we can place more proteins in a box
app = App('test').use('Initial')
box = app.builder.new_simulation_box(20, 20, 20).in_solvent('pure water')
mol = app.builder.protein_from_pdb('fus.pdb')
box.place_molecule_periodically(mol, 1, 1, 1)
simulation = app.simulation.new_simulation(
    box,
    'monomer',
    total_time=1 * Unit.TimeScale.ns,
    snap_shot=10,
)
simulation.run()
box.to_xml('init_fus')