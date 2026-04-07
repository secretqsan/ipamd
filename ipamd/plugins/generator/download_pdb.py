import pypdbio
from ipamd.public.utils.output import error, info
configure = {
    "schema": 'io',
}
def func(pdb_id, working_dir):
    try:
        pypdbio.fetch(
            pdb_id,
            working_dir + '/' + pdb_id + '.pdb',
        )
    except Exception as e:
        error('Failed to download ' + pdb_id + ' from RCSB. ' + str(e))
        return
    info('Downloaded ' + pdb_id + ' from RCSB.')
