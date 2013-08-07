import random, math

class Tessellation:
	def __init__(self, mapGen, lookup):
		self.mapGen = mapGen
		self.lookup = lookup
		
	def parsePoint(self, point):
		if point in self.mapGen.spawns:
			return self.lookup['spawn']
			
		elif point in self.mapGen.searched:
			return self.lookup['searched']
			
		elif self.mapGen.isWall(point):
			return self.lookup['wall']
			
		elif self.mapGen.isPlayArea(point):
			return self.lookup['play']
			
		else:
			return self.lookup['empty']
	
	def mapValues(self):
		colorMap = self.mapGen.emptyMap(self.mapGen.x, self.mapGen.y)
		
		for x in range(self.mapGen.x):
			for y in range(self.mapGen.y):
					colorMap[y][x] = self.parsePoint((x, y))
		return colorMap
