import random, math
from datetime import datetime

from MapGenerator import *
from Tessellation import *

def index(seed=300):
	import matplotlib.pyplot as plt
	import numpy as np

	m = MapGenerator(100, 100, seed)
	m.makeRandom()
	
	
	out = np.logical_xor(m.mapMatrix, True)
	plt.imshow(out, cmap='binary', interpolation='nearest')
	plt.savefig('img/initial.png')
	
	for n in xrange(3):
		m.smooth()
		out = np.logical_xor(m.mapMatrix, True)
		plt.imshow(out, cmap='binary', interpolation='nearest')
		plt.savefig('img/smothed_%s.png' % n)



index()