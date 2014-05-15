from MapGenerator import *

import matplotlib.pyplot as plt
import numpy as np

def smoothPlot(m):
	fig = plt.figure()
	fig.suptitle('No smoothing', fontsize=20, fontweight='bold')

	## Flip matrix values
	out = np.logical_xor(m.mapMatrix, True)
	plt.imshow(out, cmap='binary', interpolation='nearest')

	plt.savefig('img/initial.png')

	for n in xrange(3):
		m.smooth()

		fig = plt.figure()
		fig.suptitle('Smooth Factor - %s' % n, fontsize=20, fontweight='bold')

		out = np.logical_xor(m.mapMatrix, True)
		plt.imshow(out, cmap='binary', interpolation='nearest')

		plt.savefig('img/smothed_%s.png' % n)

	return m

seed = 300
m = MapGenerator(100, 100, seed)
m.makeRandom()

m = smoothPlot(m)
