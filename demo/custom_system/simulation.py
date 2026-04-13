from ipamd import App
from ipamd.public.models.md import Unit

app = App('custom_system')
app.use('Calvados3')
app.use({
    "atom_definition": {
        "CA": {"charge": 0, "mass": 72},
        "Nda": {"charge": 0, "mass": 72},
        "COH": {"charge": 0, "mass": 72},
        "COO": {"charge": 0, "mass": 72}
    },
    "ff_param": {
        "ah": {
            "CA": {'lambda': '1.033450123574512', 'sigma': '0.1'},
            "Nda": {'lambda': '0.4473142572693176', 'sigma': '0.1'},
            "COH": {'lambda': '0.092587557536158', 'sigma': '0.1'},
            "COO": {'lambda': '0.092587557536158', 'sigma': '0.1'}
        }
    }
}, override=False)
app.builder.load_example_molecule('fus')
box = app.builder.new_simulation_box(40, 40, 40).in_solvent('pure water')
mol = app.builder.cg_molecule_from_pdb('charged.pdb', rigid_range='1-401')
mol_fus = app.builder.protein_from_pdb('fus.pdb', rigid_range='285-371')
box.place_molecule_randomly(mol, 5)
box.place_molecule_randomly(mol_fus, 10)
simulation = app.simulation.new_simulation(
    box,
    'monomer',
    total_time=1 * Unit.TimeScale.ns,
    snap_shot=10,
)
simulation.run()
box.to_xml('final')
