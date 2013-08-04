from bottle import *
import matplotlib.pyplot as plt
import random, math, cStringIO

class MapGenerator:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
		self.mapMatrix = self.emptyMap(x, y)
	
	def emptyMap(self, x, y):
		return [[0]*x for i in range(y)]
	
	def randomCord(self):
		x = int(random.gauss(self.x/2, self.x) % self.x)
		y = int(random.gauss(self.y/2, self.y) % self.y)
		return (x, y)
	
	def neighborCord(self, point):
		ptList = []
		(x, y) = point
		for a in range(x-1, x+2):
			for b in range(y-1, y+2):
				if(a>=0 and b>=0 and a < self.x and b < self.y):
					ptList.append((a, b))
		ptList.remove(point)
		return ptList
	
	def makeRandom(self):
		for i in range(self.x * self.y):
			(x, y) = self.randomCord()
			self.mapMatrix[y][x] ^= 1
		return self
	
	def smooth(self, r=1, factor=4):
		newMap = self.emptyMap(self.x, self.y)
		
		for x in range(self.x):
			for y in range(self.y):
				i = 0
				for a in range(x-r, x+r+1):
					for b in range(y-r, y+r+1):
						i += self.mapMatrix[b%self.y][a%self.x]
						
				newMap[y][x] = i>=factor
		self.mapMatrix = newMap
		return self
	
	def isPlayArea(self, point):
		(x, y) = point
		return self.mapMatrix[y][x] == 1
	
	def isWall(self, point):
		if not self.isPlayArea(point):
			return False
		
		neighbors = self.neighborCord(point)
		allNeighborsPlayable = len(neighbors) == 8
		for n in neighbors:
			allNeighborsPlayable &= self.isPlayArea(n)
		return not allNeighborsPlayable
		
	
	def matrix(self):
		return self.mapMatrix
	
	def size(self):
		return (self.x, self.y)
	
	def colorize(self):
		colorMap = self.emptyMap(self.x, self.y)
		for x in range(self.x):
			for y in range(self.y):
				if self.isWall((x, y)):
					colorMap[y][x] = [1, 0, 0]
				elif self.isPlayArea((x, y)):
					colorMap[y][x] = [1, 1, 1]
				else:
					colorMap[y][x] = [0, 0, 0]
		return colorMap
	
	def show(self):
		plt.imshow(self.colorize(), interpolation='nearest')
		plt.ylim([0, self.y])
		plt.xlim([0, self.x])
		plt.show()

@route('/<seed>.png')
def index(seed=300):
	response.content_type = "image/png"
	random.seed(seed)
	m = MapGenerator(100, 100)
	m.makeRandom().smooth().smooth().smooth()
	
	plt.imshow(m.colorize(), interpolation='nearest')
	plt.ylim([0, m.y])
	plt.xlim([0, m.x])
	
	output = cStringIO.StringIO()
	plt.savefig(output, format="png")
	return output.getvalue()

run(host='localhost', port=8081)