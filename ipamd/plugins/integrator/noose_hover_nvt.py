def func(param, all_info, group, gala_core):
    comp_info = gala_core.ComputeInfo(all_info, group)
    t_reduced = param['temperature'] * 8.3143 / 1000.0
    rigid = param['rigid']
    integrator = None
    if rigid:
        integrator = gala_core.NVTRigid(all_info, group, t_reduced, 0.05)
    else:
        integrator = gala_core.NoseHooverNVT(all_info, group, comp_info, t_reduced, 0.05)
    return integrator
