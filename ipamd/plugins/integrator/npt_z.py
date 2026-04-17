def func(param, all_info, group, gala_core):
    all_group = gala_core.ParticleSet(all_info, 'all')
    comp_info_group = gala_core.ComputeInfo(all_info, group)
    comp_info_all = gala_core.ComputeInfo(all_info, all_group)
    t_reduced = param['temperature'] * 8.3143 / 1000.0
    p = param['pressure']
    rigid = param['rigid']
    integrator = None
    if rigid:
        integrator = gala_core.NPTMTKRigid(
            all_info, group, comp_info_group, comp_info_all, t_reduced, p, 0.5, 1.0
        )

    else:
        integrator = gala_core.NPTMTK(
            all_info, group, comp_info_group, comp_info_all, t_reduced, p, 0.5, 1.0
        )
    integrator.setSemiisotropic(0, p)
    integrator.setCompressibility(0, 0, 7.47e-4)
    return integrator
