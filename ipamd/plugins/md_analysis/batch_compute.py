from ipamd.public.utils.plugin_manager_v1 import PluginBase
def func(box, target_frame, type1='', type2='', threshold=4, mode='inter', cm=None):
    if cm is None:
        cm = PluginBase.call(
            'contact_map_v1',
            box=box,
            target_frame=target_frame,
            type1=type1,
            type2=type2,
            threshold=threshold,
            mode=mode
        )
    cn = PluginBase.call(
        'flatten',
        cm,
        module = 'data_process',
        axis = 1
    )
    cn.meta['y_label'] = f'Contact Number'
    cn.meta['title'] = f'Contact Number'
    return cn