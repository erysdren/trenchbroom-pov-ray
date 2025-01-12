#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

class Vec2():
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
	def __repr__(self):
		return f"{self.x} {self.y}"

class Vec3():
	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z
	def __repr__(self):
		return f"{self.x} {self.y} {self.z}"

class Vec4():
	def __init__(self, x=0, y=0, z=0, w=0):
		self.x = x
		self.y = y
		self.z = z
		self.w = w
	def __repr__(self):
		return f"{self.x} {self.y} {self.z} {self.w}"

class Plane():
	def __init__(self, x=Vec3(), y=Vec3(), z=Vec3()):
		self.x = x
		self.y = y
		self.z = z
	def __repr__(self):
		return repr(self.x) + repr(self.y) + repr(self.z)

class MapEntity(dict):
	def __init__(self, brushes=[]):
		self.brushes = brushes

class MapBrushFace():
	def __init__(self, plane=Plane(), texture="", u=Vec4(), v=Vec4(), scale=Vec2()):
		self.plane = plane
		self.texture = texture
		self.u = u
		self.v = v
		self.scale = scale
	def __repr__(self):
		return repr(self.plane) + self.texture + repr(self.u) + repr(self.v) + repr(self.scale)

class MapBrush():
	def __init__(self, faces=[]):
		self.faces = faces
	def __repr__(self):
		return repr(self.faces)

# print something useful then quit
def printHelp():
	print("python3 tb2pov.py INPUT.MAP OUTPUT.POV OUTPUT.INI")
	sys.exit(0)

# parse trenchbroom header info
def parseMapHeader(inputFile):
	inputFile.seek(0)

	gameLine = inputFile.readline()
	formatLine = inputFile.readline()

	mapGame = gameLine.split("Game:")[1].strip()
	mapFormat = formatLine.split("Format:")[1].strip()

	return mapGame, mapFormat

# parse brush
def parseBrush(inputFile):
	mapBrush = MapBrush()
	while True:
		line = inputFile.readline()
		if not line:
			die("Early EOF")
		# brush face
		if line.startswith("("):
			mapBrushFace = MapBrushFace()
			tokens = line.split()
			mapBrushFace.plane.x.x = float(tokens[1])
			mapBrushFace.plane.x.y = float(tokens[2])
			mapBrushFace.plane.x.z = float(tokens[3])
			mapBrushFace.plane.y.x = float(tokens[6])
			mapBrushFace.plane.y.y = float(tokens[7])
			mapBrushFace.plane.y.z = float(tokens[8])
			mapBrushFace.plane.z.x = float(tokens[11])
			mapBrushFace.plane.z.y = float(tokens[12])
			mapBrushFace.plane.z.z = float(tokens[13])
			mapBrushFace.texture = tokens[15]
			mapBrushFace.u.x = float(tokens[17])
			mapBrushFace.u.y = float(tokens[18])
			mapBrushFace.u.z = float(tokens[19])
			mapBrushFace.u.w = float(tokens[20])
			mapBrushFace.v.x = float(tokens[23])
			mapBrushFace.v.y = float(tokens[24])
			mapBrushFace.v.z = float(tokens[25])
			mapBrushFace.v.w = float(tokens[26])
			mapBrushFace.scale.x = float(tokens[29])
			mapBrushFace.scale.y = float(tokens[30])
			mapBrush.faces.append(mapBrushFace)
		# done with brush
		elif line.startswith("}"):
			return mapBrush

# parse map entity from current position in input file
def parseEntity(inputFile):
	mapEntity = MapEntity()
	while True:
		line = inputFile.readline()
		if not line:
			die("Early EOF")
		# key/value pair
		if line.startswith("\""):
			key = line.split("\"")[1]
			value = line.split("\"")[3]
			mapEntity[key] = value
		# brush
		elif line.startswith("{"):
			mapEntity.brushes.append(parseBrush(inputFile))
		# done with entity
		elif line.startswith("}"):
			return mapEntity

# parse map map file into an array of entities
def parseMapEntities(inputFile):
	inputFile.seek(0)

	mapEntities = []

	while True:
		# read a line
		line = inputFile.readline()
		# end of file
		if not line:
			break
		# comment
		if line.startswith("//"):
			continue
		elif line.startswith("{"):
			mapEntities.append(parseEntity(inputFile))

	return mapEntities

# oopsie, we gotta bail
def die(msg):
	print(f"ERROR: {msg}")
	sys.exit(1)

# start here
if __name__ == "__main__":

	if len(sys.argv) != 4:
		printHelp()

	inputFile = open(sys.argv[1], "r")
	if not inputFile:
		die(f"Failed to open {sys.argv[1]}")

	# parse trenchbroom header info
	mapGame, mapFormat = parseMapHeader(inputFile)

	# check validity
	if mapGame != "POV-Ray" or mapFormat != "Valve":
		die(f"{sys.argv[1]} is not set up correctly for this tool (invalid Game or Format)")

	# parse map structure
	mapEntities = parseMapEntities(inputFile)
