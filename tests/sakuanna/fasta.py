from ipamd import App
from ipamd.public.models.sequence import ProteinSequence

app = App('tests')
app.gen_link()
seq = ProteinSequence(name='a', sequence='ACDEFGHIKLMNPQRSTVWY' * 20)

app.sakuanna.to_fasta(seq)

seq = app.sakuanna.sequence_from_fasta('a.fasta')