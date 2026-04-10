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

rna = RNASequence('U15A15', 'AUCGCGAU')
rna_mol = app.builder.molecule_from_curve(
    rna,
    lambda index: (0, 0, index * 0.5) if index < 4 else (0, 1.13, (7 - index) * 0.5),
    rename_map={
        'C': 'Cd',
        'G': 'Gd',
        'A': 'Ad',
        'U': 'Ud',
    },
    new_bond="R-R"
)
for n in range(2):
    rna_mol.link(n, 7 - n, type_="RS")

app.load_file('dimer_G3BP1.pdb')
prot = app.builder.protein_from_pdb(
    'dimer_G3BP1.pdb',
    rigid_range='0-200'
)
app.builder.mpipi_chtype(prot)

box.place_molecule_randomly(prot, 1, allow_out_of_box=False)
box.place_molecule_randomly(rna_mol, 1, allow_out_of_box=False)
simulation.run()
