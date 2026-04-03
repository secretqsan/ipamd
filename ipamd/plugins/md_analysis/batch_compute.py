from ipamd.public.utils.plugin_manager_v1 import PluginBase
from ipamd.public.utils.parser import range_to_list
def func(function, box, target_frame, **kargs):
    results = []
    for frame in range_to_list(target_frame):
        results.append(
            PluginBase.call(function, box=box, target_frame=frame, **kargs)
        )
    res = PluginBase.call(
        'average',
        *results,
        module='data_process'
    )

    return res