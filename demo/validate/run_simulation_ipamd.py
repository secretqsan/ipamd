from ipamd import App

nx = 200
ny = 100
nz = 100
app = App('cmp_openmm', gpu_id=1).use('Calvados3')
mol = app.builder.linear_protein('sg', 'G')
box = app.builder.new_simulation_box(nx, ny, nz).in_solvent('pure water')
box.place_molecule_periodically(mol, nx, ny, nz)
simulation = app.simulation.new_simulation(box, str(nx * ny * nz), total_time=50, snap_shot=2, res_auto_read=False, minimize_energy=False)
simulation.run()