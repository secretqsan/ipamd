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
box = app.builder.box_from_xml('final')
simulation = app.simulation.new_simulation(
    box,
    'continue',
    total_time=1 * Unit.TimeScale.ns,
    snap_shot=10,
    minimize_energy=False
)
simulation.run()
