from ipamd import App
from ipamd.public.models.sequence import ProteinSequence

app = App('sequence_analysis', gpu_id=0)
sequence = ProteinSequence(name='test', sequence='ACDEFGHIKLMNPQRSTVWY')
app.sakuanna.pretier(sequence, word3=True, ter=True)
res = app.sakuanna.statistic(sequence, targets=['A', 'charged'], format_='ratio')
app.data_process.plot(res)
