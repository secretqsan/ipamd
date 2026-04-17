from ipamd import App
from ipamd.public.models.sequence import RNASequence
from ipamd.public.models.md import Unit
app = App('RNA_Protein', gpu_id=7).use('mpipi')
app.gen_link()
box = app.builder.new_simulation_box(40, 40, 40).in_solvent('normal saline')
simulation = app.simulation.new_simulation(
    box,
    'RNA_Protein',
    total_time=10 * Unit.TimeScale.ns,
    snap_shot=10
)

rna = RNASequence('rna', 'A' * 15 + 'U' * 15)
rna_mol = app.builder.molecule_from_curve(
    rna,
    lambda index: (0, 0, index * 0.5) if index < 15 else (0, 1.13, (29 - index) * 0.5),
    rename_map={
        'A': 'Ad',
        'U': 'Ud',
    },
    new_bond="R-R"
)
for n in range(4):
    rna_mol.link(n, 29 - n, type_="RS")

app.load_file('dimer_G3BP1.pdb')
prot = app.builder.protein_from_pdb(
    'dimer_G3BP1.pdb',
    rigid_range='0-139,466-605;340-413;806-879'
)
app.builder.mpipi_chtype(prot)

box.place_molecule_randomly(prot, 10, allow_out_of_box=False)
box.place_molecule_randomly(rna_mol, 10, allow_out_of_box=False)
simulation.run()
