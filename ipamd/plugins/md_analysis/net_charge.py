from ipamd.public.models.data import Scalar
configure = {
    "schema": ['frame'],
}
def func(frame, **kwargs):
    prop = frame.properties(ignoring_image=False)
    charge = 0
    for mol in prop['molecules']:
        charge += sum(mol['charge'])

    return Scalar(
        data=charge,
        title='net charge',
        unit='e'
    )