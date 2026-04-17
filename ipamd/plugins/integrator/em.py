def func(param, all_info, group, gala_core):
    rigid = param['rigid']
    integrator = None
    if rigid:
        integrator = gala_core.NVERigid(all_info, group)
    else:
        integrator = gala_core.NVE(all_info, group)
    integrator.setZeroVel(True, 5)
    integrator.setLimit(0.001)
    return integrator
