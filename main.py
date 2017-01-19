from PIL import Image
import sys, numpy, time, os
class Node(object):
	distance = 0
	end = False
	start = False
	pathItem = False
	
	
	def __init__(self, color, position):
		self.color = color;
		self.position = position
		if color == "0, 0, 0":
			self.passable = False
		else:
			self.passable = True
	
	
	def colorVector(self):
		return self.color.replace(" ", "").split(",")
	
	def updateDistance(self, end):
		diffX = abs(end[0]-self.position[0])
		diffY = abs(end[1]-self.position[1])
		self.distance = diffX+diffY
		if self.distance < 10:
			self.distance = "0"+str(self.distance)
		else:
			self.distance = str(self.distance)
			
			
	def checkAround(self):
		#returns how many available nodes are passable around self. Excluding diagonal
		counter = []
		x = self.position[0]
		y = self.position[1]
		if x < width-1:
			if map[y][x+1].passable:
				counter.append("r")
		if x > 0:
			if map[y][x-1].passable:
				counter.append("l")
		if y < height-1:
			if map[y+1][x].passable:
				counter.append("d")
		if y > 0:
			if map[y-1][x].passable:
				counter.append("u")
		
		return counter
		


def printMap(show="all"):
	offset=" "*2 #
	print("\n" + offset, end="")
	for i in range(width):
		print(str(i), end="")
		if i < 10:
			print("   ", end="")
		else:
			print("    ", end="")
	
	print("\n" + offset, end="")
	print("_"*width*4)
	
	for y in range(height):
		print(str(y) + "|", end="")
		for x in range(width):
			if show == "start":
				if map[y][x].start:
					print("S   ", end="")
				else:
					print("   ", end="")
			elif show == "end":
				if map[y][x].end:
					print("E   ", end="")
				else:
					print("   ", end="")
			elif show == "passable":
				if not map[y][x].passable:
					print("■   ", end="")
				else:
					print("    ", end="")
			else:
				if map[y][x].color == "255, 255, 255":
					if show == "distance":
						print(map[y][x].distance + " ", end="")
					else:
						print("    ", end="")
						
				elif map[y][x].color == "0, 0, 0":
					print("■   ", end="")
				elif map[y][x].color == "0, 255, 0":
					print("S   ", end="")
				elif map[y][x].color  == "255, 0, 0":
					print("E   ", end="")
				elif map[y][x].color  == "0, 0, 255":
					print("*   ", end="")
		print("")

def mapToImage(outputName):		  
	output = []
	for y in range(height):
		output.append([])
		for x in range(width):
			output[y].append(map[y][x].colorVector())
				
	Image.fromarray(numpy.uint8(output)).save(outputName + ".png")
	
def findPath(map, start, end):
	foundFinish = False

	lowestDistance = width+height
	path = []
	currentNode = map[start[1]][start[0]]
	nextNode = "unknown"
	iterations = 0
	
	while not foundFinish:
		path.append(currentNode)
		
		if currentNode.checkAround() == []:
			currentNode = map[start[1]][start[0]]
			for i in path:
				map[i.y][i.x].passable = True
			
			map[path[len(path)-1].y][path[len(path)-1].x].passable = False
			
			
			path = []
			
		
		
		for i in currentNode.checkAround():
			
			if currentNode.x < width-1:
				if i == 'r':
					if int( map[currentNode.y][currentNode.x+1].distance ) < lowestDistance:
						lowestDistance = int(map[currentNode.y][currentNode.x+1].distance)
						nextNode = map[currentNode.y][currentNode.x+1]
						
			
			if currentNode.x > 0:
				if i == 'l':
					if int( map[currentNode.y][currentNode.x-1].distance ) < lowestDistance:
						lowestDistance = int(map[currentNode.y][currentNode.x-1].distance)
						nextNode = map[currentNode.y][currentNode.x-1]
			
			if currentNode.y < height-1:	
				if i == 'd':
					if int( map[currentNode.y+1][currentNode.x].distance ) < lowestDistance:
						lowestDistance = int(map[currentNode.y+1][currentNode.x].distance)
						nextNode = map[currentNode.y+1][currentNode.x]
			
			if currentNode.y > 0:
				if i == 'u':
					if int( map[currentNode.y-1][currentNode.x].distance ) < lowestDistance:
						lowestDistance = int(map[currentNode.y-1][currentNode.x].distance)
						nextNode = map[currentNode.y-1][currentNode.x]
		
		
		if currentNode.checkAround() == [] and path == []:
			print("Could not find path!")
			break	
		
		
		currentNode.passable = False
		currentNode = nextNode
		lowestDistance = width+height
		
		if currentNode.distance == "00":
			foundFinish = True
		
		iterations += 1


	#output found path
	for i in path:
		if not map[i.y][i.x].start:
			map[i.y][i.x].color = "0, 0, 255"

while 1:
	image = Image.open("map1.png")
	width, height = image.size
	image_data = list(image.getdata())

	for i in range(len(image_data)):#make data easier to handle
		image_data[i] = Node(str(image_data[i]).replace("(", "").replace(")", ""), [0, 0])#create Node objects

	map = []
	for i in range(width):#change image_data into matrix of Nodes with correct width
		map.append(image_data[i*width:width*(i+1)])#object can be accessed by map[y][x]



	start = []
	end = []
	for y in range(height):
		for x in range(width):
			if map[y][x].color == '0, 255, 0':#set start position
				if start == []:
					start = [x, y]
					map[y][x].start = True
				else:
					print("Error: Cannot have more than one start")
					sys.exit()
			elif map[y][x].color == '255, 0, 0':#set end position
				if end == []:
					end = [x, y]
					map[y][x].end = True
				else:
					print("Error: Cannot have more than one end")
					sys.exit()
	if start == []:
		print("Error: Could not find start")
		sys.exit()
	elif end == []:
		print("Error: Could not find end")
		sys.exit()

	#now start and end are found, update Node 
	for y in range(height):
		for x in range(width):
			map[y][x].position = [x, y]
			map[y][x].x = x
			map[y][x].y = y
			map[y][x].updateDistance(end)

	
	os.system("clear")
	print("Finding path...")
	findPath(map, start, end)
	mapToImage("output")
		
	time.sleep(1)


















