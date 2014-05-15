from MapGenerator import *

import matplotlib.pyplot as plt
import numpy as np


def index(seed=300):
	m = MapGenerator(100, 100, seed)
	m.makeRandom()
	
	fig = plt.figure()
	fig.suptitle('No smoothing', fontsize=20, fontweight='bold')
	
	out = np.logical_xor(m.mapMatrix, True)
	plt.imshow(out, cmap='binary', interpolation='nearest')
	plt.savefig('img/initial.png')
	
	for n in xrange(3):
		fig = plt.figure()
		fig.suptitle('Smooth Factor - %s' % n, fontsize=20, fontweight='bold')
		m.smooth()
		out = np.logical_xor(m.mapMatrix, True)
		plt.imshow(out, cmap='binary', interpolation='nearest')
		plt.savefig('img/smothed_%s.png' % n)



index()