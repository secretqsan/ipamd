from ipamd import App
from ipamd.public.models.md import Unit
app = App('example',gpu_id=0)
app.gen_link()
app.use('Calvados3')
box = app.builder.new_simulation_box(40, 40, 80).in_solvent('pure water')
box.read_xml('init')
simulation = app.simulation.new_simulation(
    box,
    'production',
    total_time=20*Unit.TimeScale.ns,
    snap_shot=40,
    minimize_energy=False
)
simulation.run()
mda = app.mdanalysis
dp = app.data_process
density = mda.batch_compute(
    'density_align',
    box=box,
    target_frame='21-40'
)
dp.plot(density, save_figure=True)
free_energy = mda.slab_free_energy(
    box=box,
    target_frame='21-40',
)
dp.print(free_energy, precision=8)