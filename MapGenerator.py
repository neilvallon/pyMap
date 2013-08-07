import random, math

class MapGenerator:
	def __init__(self, x, y, seed):
		self.x = x
		self.y = y
		self.rand = random.Random(seed)
		
		self.mapMatrix = self.emptyMap(x, y)
	
	def emptyMap(self, x, y):
		return [[0]*x for i in range(y)]
	
	def randomCord(self):
		x = int(self.rand.uniform(0, self.x-1)) % self.x#int(self.rand.normalvariate(self.x/2, self.x) % self.x)
		y = int(self.rand.uniform(0, self.y-1)) % self.y#int(self.rand.normalvariate(self.y/2, self.y) % self.y)
		return (x, y)
	
	def randomPlayable(self):
		point = self.randomCord()
		while not self.isPlayArea(point):
			point = self.randomCord();
		return point
	
	def neighborCord(self, point):
		ptList = []
		(x, y) = point
		for a in range(x-1, x+2):
			for b in range(y-1, y+2):
				if(a>=0 and b>=0 and a < self.x and b < self.y):
					ptList.append((a, b))
		ptList.remove(point)
		return ptList
	
	def manhatanDist(self, pt1, pt2):
		return abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])
	
	def moveableNeighbors(self, point):
		(x, y) = point
		ptList = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
		return filter(self.isPlayArea, ptList)
	
	def makeRandom(self):
		for i in range(int(self.x * self.y * 0.75)):
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
	
	def nearestPlayable(self, point):
		frontier = [point]
		explored = []
		while frontier:
			node = frontier.pop(0)
			if self.isPlayArea(node):
				return node
				
			neighbors = self.neighborCord(node)
			toAdd = filter(lambda x: not (x in frontier or x in explored), neighbors)
			
			frontier.extend(toAdd)
			explored.append(node)
	
	def removeIslands(self):
		newMap = self.emptyMap(self.x, self.y)
		
		point = self.randomPlayable()
		
		frontier = [point]
		explored = []
		while frontier:
			node = frontier.pop()
			neighbors = self.moveableNeighbors(node)
			toAdd = filter(lambda x: not (x in frontier or x in explored), neighbors)
			
			frontier.extend(toAdd)
			explored.append(node)
			newMap[node[1]][node[0]] = 1
		
		self.mapMatrix = newMap
		return self
	
	def removeIslands_n(self):
		newMap = self.emptyMap(self.x, self.y)
		(start, goal) = self.spawns
		
		frontier = [(start, self.manhatanDist(start, goal))]
		explored = []
		while frontier:
			frontier.sort(key=lambda tup: tup[1], reverse=True)
			(node, weight) = frontier.pop()
			
			if node == goal:
				self.searched = explored
				return self
			
			neighbors = self.moveableNeighbors(node)
			toAdd = filter(lambda x: not (x in explored), neighbors)
			
			toAddW = map(lambda x: (x, self.manhatanDist(x, goal)), toAdd)
			
			frontier.extend(toAddW)
			explored.extend(toAdd)
			newMap[node[1]][node[0]] = 1
		
		self.searched = explored
		self.mapMatrix = newMap
		self.findSpawns()
		return self
	
	def findSpawns(self):
		posibleSpawns = self.playableCords()
		s1 = self.randomPlayable()
		s2 = self.randomPlayable()
		
		for i in range(20):
			s1acum = (0, 0)
			s2acum = (0, 0)
			s1c = 0
			s2c = 0
			
			deadCord = ( (int( (s1[0]+s2[0]) / 2) ), (int( (s1[1]+s2[1]) / 2 )) )
			
			for s in posibleSpawns:
				s1Dis = self.manhatanDist(s, s1)
				s2Dis = self.manhatanDist(s, s2)
				deadDis = self.manhatanDist(s, deadCord)/2
				if s1Dis < s2Dis:
					if deadDis < s1Dis: continue
					s1c += 1
					s1acum = (s1acum[0] + s[0], s1acum[1] + s[1])
				else:
					if deadDis < s2Dis: continue
					s2c += 1
					s2acum = (s2acum[0] + s[0], s2acum[1] + s[1])
			
			s1 =  (s1acum[0] / s1c, s1acum[1] / s1c)
			s2 =  (s2acum[0] / s2c, s2acum[1] / s2c)
		
		s1 = self.nearestPlayable( (int(s1[0]), int(s1[1])) )
		s2 = self.nearestPlayable( (int(s2[0]), int(s2[1])) )
		self.spawns = (s1, s2)
		return self
	
	def isPlayArea(self, point):
		(x, y) = point
		if(x<0 or y<0 or x >= self.x or y >= self.y):
			return False
		return self.mapMatrix[y][x] == 1
	
	def isWall(self, point):
		neighbors = self.neighborCord(point)
		if self.isPlayArea(point):
			return len(neighbors) != 8
		
		allNeighborsPlayable = False
		for n in neighbors:
			allNeighborsPlayable |= self.isPlayArea(n)
		return allNeighborsPlayable
	
	def playableCords(self):
		ptLst = []
		for y in range(self.y):
			for x in range(self.x):
				if self.isPlayArea((x, y)):
					ptLst.append((x, y))
		return ptLst
	
	def matrix(self):
		return self.mapMatrix
	
	def size(self):
		return (self.x, self.y)
