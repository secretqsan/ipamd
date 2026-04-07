from ipamd import App
from ipamd.public.models.sequence import RNASequence
from ipamd.public.models.md import Unit
app = App('test', gpu_id=2).use('mpipi')
box = app.builder.new_simulation_box(40, 40, 40).in_solvent('normal saline')
simulation = app.simulation.new_simulation(
    box, 'molecule_from_curve_test', total_time=1 * Unit.TimeScale.ns, snap_shot=4
)

rna = RNASequence('U15A15', 'U' * 15 + 'A' * 15)
rna_mol = app.builder.molecule_from_curve(
    rna,
    lambda index: (0, 0, index * 0.5) if index < 15 else (0, 1.13, (29 - index) * 0.5),
    rename_map={
        'U': 'Ud',
        'A': 'Ad'
    },
    new_bond="R-R"
)
for n in range(5):
    rna_mol.link(n, 29 - n, type_="RS")

app.builder.load_example_molecule('fus')
fus = app.builder.protein_from_pdb('fus.pdb', rigid_range='285-371')
app.builder.mpipi_chtype(fus)

box.place_molecule_randomly(fus, 5)
box.place_molecule_randomly(rna_mol, 5)
simulation.run("y")
