def func(ff_param, all_info, gala_core):
    """
    Centripetal force loader
    """
    group = gala_core.ParticleSet(all_info, "all")
    centripetal_force = gala_core.CentripetalForce(all_info, group)
    centripetal_force.setForce(
        ff_param['shape'],
        'Z',
        float(ff_param['f']),
        float(ff_param['threshold'])
    )
    return centripetal_force
