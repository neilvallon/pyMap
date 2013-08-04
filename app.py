from bottle import *
import matplotlib.pyplot as plt
import random, math, os, cStringIO

class MapGenerator:
	def __init__(self, x, y, seed):
		self.x = x
		self.y = y
		self.rand = random.Random(seed)
		
		self.mapMatrix = self.emptyMap(x, y)
	
	def emptyMap(self, x, y):
		return [[0]*x for i in range(y)]
	
	def randomCord(self):
		x = int(self.rand.normalvariate(self.x/2, self.x) % self.x)
		y = int(self.rand.normalvariate(self.y/2, self.y) % self.y)
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
	
	def imageform(self):
		colorMap = self.emptyMap(self.x, self.y)
		for x in range(self.x):
			for y in range(self.y):
				if self.isWall((x, y)):
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

@route('/<seed>')
def index(seed=300):
	m = MapGenerator(50, 50, seed)
	m.makeRandom().smooth().smooth().smooth()
	
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
		</style>
		</head>
		<body>
		<center>
		<table>
	"""
	
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