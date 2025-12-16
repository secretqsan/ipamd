import hoomd
import numpy as np
import time

nx, ny, nz = 50, 50, 50
device = hoomd.device.GPU()
sim = hoomd.Simulation(device=device)
sim.seed = 42
coordinates = np.array([(i + 0.5 - nx / 2, j + 0.5 - ny / 2, k + 0.5 - nz / 2)
                        for i in range(nx)
                        for j in range(ny)
                        for k in range(nz)], dtype=np.float32)
snapshot = hoomd.Snapshot()
snapshot.particles.N = nx * ny * nz
snapshot.particles.position[:] = coordinates
snapshot.particles.typeid[:] = [0] * (nx * ny * nz)
snapshot.particles.mass[:] = [75.05] * (nx * ny * nz)
snapshot.particles.types = ['A']
snapshot.configuration.box = [nx, ny, nz, 0, 0, 0]
sim.create_state_from_snapshot(snapshot)
cell = hoomd.md.nlist.Cell(buffer=0.4)
rc = 4.0
s = 0.45
l = 0.701271367797246
eps = 0.8368
r_min = 0.1  # 最小距离（避免除以0）
r_array = np.linspace(r_min, rc, 1000)  # 在 r_min 到 rc 间采样1000个点
energy_array = []
force_array = []
for r in r_array:
    r0 = (2 ** (1 / 6)) * s  # LJ 平衡距离
    shift = (s / rc) ** 12 - (s / rc) ** 6

    if r >= r0:
        energy = 4 * eps * l * ((s / r) ** 12 - (s / r) ** 6 - shift)
        force = 4 * eps * l * (12 * (s ** 12) / (r ** 13) - 6 * (s ** 6) / (r ** 7))
    else:
        energy = 4 * eps * ((s / r) ** 12 - (s / r) ** 6 - l * shift) + eps * (1 - l)
        force = 4 * eps * (12 * (s ** 12) / (r ** 13) - 6 * (s ** 6) / (r ** 7))

    energy_array.append(energy)
    force_array.append(-force)
pair = hoomd.md.pair.Table(nlist=cell, default_r_cut=rc)
pair.params[('A', 'A')] = {
    'r_min': r_min,  # 最小距离
    'U': energy_array,  # 能量表
    'F': force_array  # 力表
}
integrator = hoomd.md.Integrator(dt=0.01)
langevin = hoomd.md.methods.Langevin(
    filter=hoomd.filter.All(),  # 所有粒子受力
    kT=273 * 1.380649e-23,  # 模拟温度
    default_gamma=0.001  # 阻尼系数
)
integrator.forces.append(pair)
integrator.methods.append(langevin)
sim.operations.integrator = integrator
time_start = time.time()
sim.run(3000)
time_end = time.time()
print(f"Simulation time: {time_end - time_start} seconds")