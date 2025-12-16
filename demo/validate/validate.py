from ipamd import OmicsLoader, batch_run
from ipamd.public.models.md import Environment
import csv

simu_condition = {}
with open('input_data/simu_condition.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        protein_name = row[0].strip()
        temperature = float(row[1])
        cs = float(row[2])
        ph = float(row[3])
        rang = row[4].strip().replace(";", ",")
        gap = int(row[5]) if row[5] != '' else 0
        simu_condition[protein_name] = (temperature, cs, ph, rang, gap)

loader = OmicsLoader(path='input_data/pdbs')
def process_sequence(app, data, output_file):
    app.use('Calvados3')
    box = app.builder.new_simulation_box(100, 100, 100)
    env = Environment('pure water')
    env.set_temperature(simu_condition[data['name']][0])
    env.set_ionic_strength(simu_condition[data['name']][1])
    env.set_ph(simu_condition[data['name']][2])
    box.in_solvent(env)
    #app.builder.af2(data['name'], data['sequence'])
    mol = app.builder.protein_from_pdb(data['name'] + '.pdb', rigid_range=simu_condition[data['name']][3])
    if simu_condition[data['name']][3] != '':
        mol, extra_ff = app.builder.gen_elastic_network(mol, max_gap=simu_condition[data['name']][4])
        app.use(extra_ff)
    box.place_molecule_periodically(mol, 1, 1, 1)
    simulation = app.simulation.new_simulation(box, f'{data['name']}', total_time='202ns', snap_shot=2020)
    simulation.clean_cache()
    simulation.run()
    rg2 = box.compute(app.analysis.rg, title='rg', target_frame='21-2020')
    rg_avg = rg2.flatten()
    rg_avg.print()
    with open(output_file, 'a') as f:
        f.write(f'{data["name"]},{rg_avg.data}\n')

batch_run(loader, process_sequence, gpus='1,2,3', output_file='results_cal.csv')