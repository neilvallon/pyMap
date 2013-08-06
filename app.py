from bottle import *
import matplotlib.pyplot as plt
import random, math, os, cStringIO
from datetime import datetime

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
	
	def findSpawns(self):
		posibleSpawns = self.playableCords()
		s1 = self.randomPlayable()
		s2 = self.randomPlayable()
		
		for i in range(3): ## Do 3 iterations
			s1acum = (0, 0)
			s2acum = (0, 0)
			s1c = 0
			s2c = 0
			
			for s in posibleSpawns:
				s1Dis = self.manhatanDist(s, s1)
				s2Dis = self.manhatanDist(s, s2)
				if s1Dis < s2Dis:
					s1c += 1
					s1acum = (s1acum[0] + s[0], s1acum[1] + s[1])
				else:
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
	
	def imageform(self):
		colorMap = self.emptyMap(self.x, self.y)
		for x in range(self.x):
			for y in range(self.y):
				if (x, y) in self.spawns:
					colorMap[y][x] = 'dropper_front_horizontal.png'
				elif self.isWall((x, y)):
					colorMap[y][x] = 'stonebrick_mossy.png'
				elif self.isPlayArea((x, y)):
					colorMap[y][x] = 'sand.png'
				else:
					colorMap[y][x] = 'wool_colored_black.png'
		return colorMap
	
	def show(self):
		plt.imshow(self.colorize(), interpolation='nearest')
		plt.ylim([0, self.y])
		plt.xlim([0, self.x])
		plt.show()


@get('/img/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='static/img')

@route('/<seed>.png')
def index(seed=300):
	response.content_type = "image/png"
	m = MapGenerator(100, 100, seed)
	m.makeRandom().smooth().smooth().smooth()
	
	fig = plt.imshow(m.colorize(), interpolation='nearest')
	
	#plt.set_axis_off()
	plt.axis('off')
	
	output = cStringIO.StringIO()
	plt.savefig(output, format="png", facecolor='black', dpi=300)
	return output.getvalue()

@route('/<width>x<height>/<seed>')
def index(width=50, height=50, seed=300):
	tstart = datetime.now()
	m = MapGenerator(int(width), int(height), seed)
	m.makeRandom().smooth().smooth().smooth().removeIslands().findSpawns()
	
	tdelta = datetime.now()-tstart
	
	html = """
		<html>
		<head>
		<title>pymap</title>
		<style>
		table, tr, td, img{
		border:none;
		padding:0px;
		margin:-1px;
		}
		body{
			background-image:URL("/img/wool_colored_black.png");
		}
		h2{
		color:white;
		}
		</style>
		</head>
		<body>"""
	
	html += "<h2>Generated in: "+str(tdelta)+"</h2>"
	
	html += """
		<center>
		<table>"""
	
	for y in m.imageform():
		html += "<tr>"
		for x in y:
			html += "<td><img src='/img/"+x+"' /></td>"
		html += "</tr>"
	
	
	html += """
	</table>
	</center>
	</body>
	</html>
	"""
	
	return html


@route('/')
def index(width=50, height=50):
	tstart = datetime.now()
	m = MapGenerator(int(width), int(height), random.random())
	m.makeRandom().smooth().smooth().smooth().removeIslands().findSpawns()
	
	tdelta = datetime.now()-tstart
	
	html = """
		<html>
		<head>
		<title>pymap</title>
		<style>
		table, tr, td, img{
		border:none;
		padding:0px;
		margin:-1px;
		}
		body{
			background-image:URL("/img/wool_colored_black.png");
		}
		h2{
		color:white;
		}
		</style>
		</head>
		<body>"""
	
	html += "<h2>Generated in: "+str(tdelta)+"</h2>"
	
	html += """
		<center>
		<table>"""
	
	for y in m.imageform():
		html += "<tr>"
		for x in y:
			html += "<td><img src='/img/"+x+"' /></td>"
		html += "</tr>"
	
	
	html += """
	</table>
	</center>
	</body>
	</html>
	"""
	
	return html

run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))