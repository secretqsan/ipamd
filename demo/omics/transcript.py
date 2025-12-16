from ipamd.public.models.md import Environment, Unit
from ipamd import OmicsLoader, batch_run

loader = OmicsLoader(path='input_data/transcription')
def process_sequence(app, data):
    app.use('Calvados3')
    box = app.builder.new_simulation_box(150, 150, 150)
    env = Environment('normal saline')
    env.set_temperature(273 + 37)
    box.in_solvent(env)
    mol = app.builder.protein_from_pdb(data['name'] + '.pdb', rigid_from_plddt=True)
    box.place_molecule_periodically(mol, 1, 1, 1)
    molecule_prop = box.current_frame().properties()['molecules'][0]
    rigid_prop = molecule_prop['rigid_group']
    total_length = len(rigid_prop)
    idr_length = 0
    for i in rigid_prop:
        if i >= 0:
            idr_length += 1
    rate = idr_length / total_length
    simulation = app.simulation.new_simulation(box, f'{data['name']}', total_time=20 * Unit.TimeScale.ns, snap_shot=100)
    simulation.run('n')
    flory = box.compute(app.analysis.flory_monomer, title='flory', target_frame='50-100')
    flory.print()
    with open('results_transcription.csv', 'a') as f:
        f.write(f'{data["name"]},{flory.data},{1 - rate}\n')

batch_run(loader, process_sequence)