from ipamd import App
from ipamd.public.models.md import Environment
app = App(name="ELP-R", gpu_id=2)
app.use('Calvados3')

box = app.builder.new_simulation_box(90, 20, 20)
env = Environment('pure water')
env.set_temperature(273)
box.in_solvent(env)
box1 = app.builder.box_from_xml('polyf-e')
box2 = app.builder.box_from_xml('polyf-r')

box.sub_box(box1, 20, 0, 0)
box.sub_box(box2, 50, 0, 0)
box.to_xml('merged')

simulation = app.simulation.new_simulation(box, 'm-calvados3', total_time='20ns', snap_shot=20)
simulation.run()