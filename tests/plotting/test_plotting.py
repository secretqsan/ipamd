from ipamd import App
from ipamd.public.models.md import Unit
from ipamd.public.models.sequence import ProteinSequence
app = App('example', gpu_id=2).use('Calvados3')
box = app.builder.new_simulation_box(20, 20, 20).in_solvent('pure water')
seq1 = ProteinSequence('F40', 'F' * 40)
seq2 = ProteinSequence('F5', 'F' * 5)
mol1 = app.builder.spiral_protein(seq1)
mol2 = app.builder.spiral_protein(seq2)
box.place_molecule_randomly(mol1, 10, strict=True)
box.place_molecule_randomly(mol2, 10, strict=True)
simulation = app.simulation.new_simulation(box, 'simulation', total_time=1*Unit.TimeScale.ns, snap_shot=2)
simulation.run()

res = app.mdanalysis.contact_map_v1(
    box=box,
    type1='F5',
    type2='F40',
    target_frame=0, threshold=4, mode='inter')
app.data_process.plot(
    res,
    save_figure=True,
    style={'figure.figsize': (10, 10)},
)
