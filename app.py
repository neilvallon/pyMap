from bottle import *
import random, math
from datetime import datetime

from MapGenerator import *
from Tessellation import *


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
	
	table = {
		'play': 'sand.png',
		'spawn': 'dropper_front_horizontal.png',
		'searched': 'planks_birch.png',
		'wall': 'stonebrick_mossy.png',
		'empty': 'wool_colored_black.png'}
	
	for y in Tessellation(m, table).mapValues():
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
	import matplotlib.pyplot as plt
	import os, cStringIO
	
	response.content_type = "image/png"
	m = MapGenerator(100, 100, seed)
	m.makeRandom().smooth().smooth().smooth().findSpawns().removeIslands_n()
	
	
	table = {
		'play': [1, 1, 1],
		'spawn': [0, 0, 1],
		'searched': [0.5, 1, 0.5],
		'wall': [1, 0, 0],
		'empty': [0, 0, 0]}
	
	fig = plt.imshow(Tessellation(m, table).mapValues(), interpolation='nearest')
	
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
