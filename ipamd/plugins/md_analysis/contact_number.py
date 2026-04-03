"""
plugin for calculating contact number
"""
from ipamd.public.utils.plugin_manager_v1 import PluginBase
def func(box=None, target_frame=None, type1='', type2='', threshold=4, mode='inter', cm=None):
    """
    main function for calculating contact number

    :param box: the simulation box
    :param target_frame: the target frame to calculate. If None, calculate for all frames.
    :param type1: the first type of molecule to calculate. If None, calculate for all types.
    :param type2: the second type of molecule to calculate. If None, calculate for all types.
    :param threshold: the threshold of the contact
    :param mode: the mode of the contact
    :param cm: the contact map to calculate. If None, calculate for all frames.

    :return: a vector containing the contact number along the axis
    """
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
    cn.meta['y_label'] = 'Contact Number'
    cn.meta['title'] = 'Contact Number'
    return cn
