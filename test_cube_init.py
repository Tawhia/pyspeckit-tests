from __future__ import print_function
import numpy as np
import pyspeckit
from astropy import units as u

mycube = np.random.randn(250,50,50)
myaxis = np.linspace(-100,100,250)
pcube=pyspeckit.Cube(cube=mycube, xarr=myaxis, xunit='km/s',
                     xarrkwargs=dict(refX=1*u.GHz, velocity_convention='radio'))
pcube.xarr.velocity_convention='radio'
pcube.xarr.refX=1*u.GHz

pcube.xarr.convert_to_unit('m/s')

sp = pcube.get_spectrum(5,5)

print(pcube)
print(pcube.__repr__())

stack = pyspeckit.CubeStack([pcube, pcube])
stack.xarr.convert_to_unit(u.km/u.s)
