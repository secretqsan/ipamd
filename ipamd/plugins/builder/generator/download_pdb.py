import requests
from ipamd.public.utils.output import *
configure = {
    "schema": 'io',
}
def func(id, working_dir):
    url = "https://files.rcsb.org/download/" + id + ".pdb"
    data = requests.get(url)
    with open(working_dir + '/' + id + '.pdb', 'wb') as f:
        f.write(data.content)
    info('Downloaded ' + id + ' from RCSB.')