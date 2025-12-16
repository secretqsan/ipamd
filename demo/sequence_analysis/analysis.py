from ipamd import App

app = App('sequence_analysis', gpu_id=0)
sequence = app.sakuanna.new_protein_sequence(name='test', sequence='ACDEFGHIKLMNPQRSTVWY')
app.sakuanna.pretier(sequence, word3=True, ter=True)
res = app.sakuanna.statistic(sequence, targets=['A', 'charged'], format_='ratio')
res.plot()