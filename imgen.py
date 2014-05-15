from MapGenerator import *
from Tessellation import *

import matplotlib.pyplot as plt
import numpy as np

colors = {
	'play':     [1, 1, 1],
	'spawn':    [1, 0, 0],
	'searched': [0.5, 1, 0.5],
	'wall':     [0, 0, 0],
	'empty':    [0, 0, 0]
	}

def smoothPlot(m):
	for n in xrange(4):
		if n > 0:
			m.smooth()

		fig = plt.figure()
		fig.suptitle('Smooth Factor - %s' % n, fontsize=20, fontweight='bold')

		out = Tessellation(m, colors).mapValues()
		plt.imshow(out, interpolation='nearest')

		plt.savefig('img/smothed_%s.png' % n)

	return m

seed = 300
m = MapGenerator(100, 100, seed)
m.makeRandom()

m = smoothPlot(m)
