from ipamd import App
from ipamd.public.models.sequence import ProteinSequence

app = App('tests')
app.gen_link()
prot = ProteinSequence(name='a', sequence='AAAFGHIKLMNPQRSTVWY' * 20)
tags = app.sakuanna.tag(prot, {'A': ['A']})
app.data_process.plot(
    tags,
    style={'figure.figsize': (10, 2)},
    appearance='discrete_heatmap'
)