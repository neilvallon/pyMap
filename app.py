from bottle import *
import matplotlib.pyplot as plt
import random, math, os, cStringIO
from datetime import datetime

from MapGenerator import *


def buildHTMLMap(seed, width, height):
	tstart = datetime.now()
	m = MapGenerator(int(width), int(height), str(seed))
	#m.makeRandom().smooth().smooth().smooth().removeIslands().findSpawns()
	m.makeRandom().smooth().smooth().smooth().findSpawns().removeIslands_n()
	
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
		h3, h4, h5{
		color:white;
		}
		</style>
		</head>
		<body>"""
	
	html += "<h3>Seed: <a href='/50x50/"+str(seed)+"'>"+str(seed)+"</a></h3>"
	html += "<h4>Generated in: "+str(tdelta)+"</h4>"
	
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
	<h5>&copy 2013 - Neil Vallon</h5>
	</center>
	</body>
	</html>
	"""
	
	return html

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
	return buildHTMLMap(seed, width, height)


@route('/')
def index(width=50, height=50):
	seed = random.random()
	return buildHTMLMap(seed, width, height)

run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))