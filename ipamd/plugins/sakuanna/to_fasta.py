from pybioseq.fasta import fastaWriter
import os

configure = {
    "resource": ['persistency_dir']
}
def func(sequence, filename='', comment='', persistency_dir=None):
    if filename == '':
        filename = os.path.join(persistency_dir, f"{sequence.name}.fasta")
    writer = fastaWriter(filename)
    writer.write(sequence.name, comment, sequence.sequence)