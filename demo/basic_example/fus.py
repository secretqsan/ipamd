from ipamd import App
from ipamd.public.models.md import Unit
app = App('example', gpu_id=0).use('Calvados3')
app.builder.load_example_molecule('fus')
box = app.builder.new_simulation_box(40, 40, 40).in_solvent('pure water')
mol = app.builder.protein_from_pdb('fus.pdb', rigid_range='285-371')
#if you want to use the elastic network, uncomment the following code:
#
#mol, extra_ff = app.builder.gen_elastic_network(mol, max_gap=4)
#app.use(extra_ff, override=False)
#
box.place_molecule_randomly(mol, 20)
simulation = app.simulation.new_simulation(
    box, 'simulation', total_time=10*Unit.TimeScale.ns, snap_shot=10
)
simulation.run()
app.data_process.plot(
    app.mdanalysis.batch_compute(
        "contact_map_v1",
        target_frame='5-10',
        box=box,
        threshold=4,
        mode='inter'
    ),
    save_figure=True
)
