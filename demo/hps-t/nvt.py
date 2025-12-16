from ipamd import App
from ipamd.public.models.md import Environment, Unit

app = App(name = 'hpst').use('HPST')
box = app.builder.new_simulation_box(50, 50, 50)
env = Environment('normal saline')
temperature = 273
env.set_temperature(temperature)
box.in_solvent(env)
box1 = app.builder.box_from_xml('slab')
box.sub_box(box1, 0, 0, 12)
simulation = app.simulation.new_simulation(box, f'simulation_{temperature}', total_time=30 * Unit.TimeScale.ns, snap_shot=30 )
simulation.run('n')
output_file = open(f'res_{temperature}.csv', 'w')
flory = box.compute(app.analysis.flory_monomer, target_frame='29-30')
output_file.write(f'{flory.data}\n')
density_list = []
density1_list = []
for frame_index in range(21, 31):
    box.frame(frame_index)
    density = box.compute(app.analysis.density, x0=0, y0=0, z0=0, lx=50, ly=50, lz=25)
    density1 = box.compute(app.analysis.density, x0=0, y0=0, z0=25, lx=50, ly=50, lz=25)
    density_list.append(density.data)
    density1_list.append(density1.data)
output_file.write(','.join(f'{density}' for density in density_list) + '\n')
output_file.write(','.join(f'{density}' for density in density1_list) + '\n')
