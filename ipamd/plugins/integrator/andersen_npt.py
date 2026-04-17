"""andersen npt integrator"""
def func(param, all_info, group, gala_core):
    """
    plugin main function
    
    :param param: parameters of the integrator
    :param all_info: all information of the system
    :param group: group of the particles
    :param gala_core: galamost_core
    :return: integrator
    """
    all_group = gala_core.ParticleSet(all_info, 'all')
    t_reduced = param['temperature'] * 8.3143 / 1000.0
    p = param['pressure']
    rigid = param['rigid']
    integrator = None
    comp_info_all = gala_core.ComputeInfo(all_info, all_group)
    comp_info_group = gala_core.ComputeInfo(all_info, group)

    if rigid:
        integrator = gala_core.NPTRigid(
            all_info, group, comp_info_group, comp_info_all, t_reduced, p, 0.5, 0.1
        )
    else:
        integrator = gala_core.NPT(
            all_info, group, comp_info_group, comp_info_all, t_reduced, p, 0.5, 0.1
        )
    return integrator
