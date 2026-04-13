from ipamd import App
from ipamd.public.models.md import Unit
app = App('example',gpu_id=0)
app.gen_link()
app.use('Calvados3')
app.use('slab_prepare', override=False)
box = app.builder.new_simulation_box(40, 40, 80).in_solvent('pure water')
app.builder.load_example_molecule('fus')
mol = app.builder.protein_from_pdb('fus.pdb', rigid_from_plddt=True)
box.place_molecule_randomly(mol, 30, strict=True)
simulation = app.simulation.new_simulation(
    box,
    'gen_conf',
    total_time=5*Unit.TimeScale.ns,
    snap_shot=4
)
simulation.run()
box.to_xml('init')
