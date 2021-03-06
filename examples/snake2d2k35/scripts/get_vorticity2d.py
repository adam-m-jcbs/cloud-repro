"""Save the vorticity field as a 2D array in HDF5 files.

PetIBM saves the vorticity at a 3D array even if the solution is 2D.
Thus, we have to re-write the vorticity solution as a 2D array.

Create a XDMF file to visualize the 2D field with VisIt.
"""

import sys
import pathlib
import numpy
import yaml

import petibmpy


name = 'wz'  # name of the field variable

# Get directories.
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output' / 'solution'
outdir = simudir / 'output' / 'postprocessing' / name
outdir.mkdir(parents=True, exist_ok=True)

# Read 3D grid and write 2D grid.
gridpath = simudir / 'output' / 'grid.h5'
x, y = petibmpy.read_grid_hdf5(gridpath, name)
gridpath = outdir / 'grid.h5'
petibmpy.write_grid_hdf5(gridpath, name, x, y)

# Get temporal parameters.
filepath = simudir / 'config.yaml'
with open(filepath, 'r') as infile:
    config = yaml.load(infile, Loader=yaml.FullLoader)['parameters']
dt = config['dt']

states = sorted([int(p.stem) for p in datadir.iterdir()])
for state in states:
    print('[time step {}]'.format(state))
    filename = '{:0>7}.h5'.format(state)
    filepath = datadir / filename
    data = petibmpy.read_field_hdf5(filepath, name)
    filepath = outdir / filename
    petibmpy.write_field_hdf5(filepath, name, data)

# Write XDMF file to visualize field with VisIt.
filepath = outdir / (name + '.xmf')
petibmpy.write_xdmf(filepath, outdir, gridpath, name, dt, states=states)
