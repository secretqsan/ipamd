from ipamd import App
app = App('ultra_large', gpu_id=3).use('Calvados1')
app.load_file('input_data/fus.pdb')
mol = app.builder.protein_from_pdb('fus.pdb', rigid_from_plddt=True)
box = app.builder.new_simulation_box(150, 150, 150)
box.in_solvent('normal saline')
box.place_molecule_randomly(mol, 512, max_tries=30)
simulation = app.simulation.new_simulation(box, 'simulation', total_time='500ns', snap_shot=50)
simulation.run()

