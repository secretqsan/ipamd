import numpy as np
from openmm import *
from openmm.app import *
import time

nx = 100
ny = 50
nz = 50
system = openmm.System()
system.setDefaultPeriodicBoxVectors(
    openmm.Vec3(nx, 0, 0) * unit.nanometer,
    openmm.Vec3(0, ny, 0) * unit.nanometer,
    openmm.Vec3(0, 0, nz) * unit.nanometer
)
topology = Topology()
topology.setUnitCellDimensions(Vec3(nx, ny, nz)*unit.nanometer)
ah = openmm.CustomNonbondedForce('select(step(r-2^(1/6)*s),4*eps*l*((s/r)^12-(s/r)^6-shift),4*eps*((s/r)^12-(s/r)^6-l*shift)+eps*(1-l)); s=0.5*(s1+s2); l=0.5*(l1+l2); shift=(0.5*(s1+s2)/rc)^12-(0.5*(s1+s2)/rc)^6')
ah.addGlobalParameter('eps', 0.8368 * unit.kilojoules_per_mole)
ah.addGlobalParameter('rc', 4.0 * unit.nanometer)
ah.addPerParticleParameter('s')
ah.addPerParticleParameter('l')
for i in range(nx * ny * nz):
    ah.addParticle([0.45 * unit.nanometer, 0.701271367797246 * unit.dimensionless])
ah.setNonbondedMethod(openmm.CustomNonbondedForce.CutoffPeriodic)
ah.setCutoffDistance(4.0 * unit.nanometer)
system.addForce(ah)
element = Element.getByAtomicNumber(1)
chain = topology.addChain()
residue = topology.addResidue("GLY", chain)
coordinates = []


for i in range(nx):
    for j in range(ny):
        for k in range(nz):
            x = i + 0.5
            y = j + 0.5
            z = k + 0.5
            system.addParticle(57.05 + 18)
            topology.addAtom("A", element, residue)
            coordinates.append([x, y, z])
coordinates = (np.array(coordinates) * unit.nanometer).astype(np.float64)
integrator = openmm.LangevinIntegrator(273 * unit.kelvin, 0.001 / unit.picosecond, 0.01 * unit.picosecond)

platform = openmm.Platform.getPlatformByName("CPU")
simulation = simulation.Simulation(
    topology, 
    system,
    integrator,
    platform
)
simulation.context.setPositions(coordinates)
time_start = time.time()
simulation.step(3000)
time_end = time.time()
print(f"Simulation time: {time_end - time_start} seconds")