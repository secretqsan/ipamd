from ipamd import App
from ipamd.public.models.md import Unit
# Run the production simulation in a larger box and proper force field
app = App('test').use('Calvados1')
box = app.builder.box_from_xml('init_condensate')

# Must run this command, or the droplet will separate due to periodic boundary conditions
box.merge_nearest()

box1 = app.builder.new_simulation_box(50, 50, 50).in_solvent('pure water')
box1.sub_box(box, 0, 0, 0)
box1.align_center()
simulation = app.simulation.new_simulation(
    box1,
    'production',
    total_time=50 * Unit.TimeScale.ns,
    snap_shot=10,
)
simulation.run()
cm = box1.compute(app.analysis.contact_map, type1='fus', target_frame='9')
cm.plot()