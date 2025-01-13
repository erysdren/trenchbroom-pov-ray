#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math

class Vec2():
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
	def __repr__(self):
		return f"[{self.x}, {self.y}]"

class Vec3():
	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z
	def __repr__(self):
		return f"[{self.x}, {self.y}, {self.z}]"

class Vec4():
	def __init__(self, x=0, y=0, z=0, w=0):
		self.x = x
		self.y = y
		self.z = z
		self.w = w
	def __repr__(self):
		return f"[{self.x}, {self.y}, {self.z}, {self.w}]"

class MapEntity(dict):
	def __init__(self):
		self.brushes = []

class MapBrushFace():
	def __init__(self):
		self.plane = Vec4()
		self.texture = ""
		self.u = Vec4()
		self.v = Vec4()
		self.scale = Vec2()
	def __repr__(self):
		return repr(self.plane) + self.texture + repr(self.u) + repr(self.v) + repr(self.scale)

class MapBrush():
	def __init__(self):
		self.faces = []
	def __repr__(self):
		return repr(self.faces)

def vec3Add(a, b):
	return Vec3(a.x + b.x, a.y + b.y, a.z + b.z)

def vec3Sub(a, b):
	return Vec3(a.x - b.x, a.y - b.y, a.z - b.z)

def vec3Length(a):
	return math.sqrt(a.x * a.x + a.y * a.y + a.z * a.z)

def vec3Normalize(a):
	mag = vec3Length(a)
	return Vec3(a.x / mag, a.y / mag, a.z / mag)

def vec3Cross(a, b):
	r = Vec3()
	r.x = a.y * b.z - a.z * b.y
	r.y = a.z * b.x - a.x * b.z
	r.z = a.x * b.y - a.y * b.x
	return r

def vec3Dot(a, b):
	r = 0
	r += a.x * b.x;
	r += a.y * b.y;
	r += a.z * b.z;
	return r

def planeFromPoints(a, b, c):
	s1 = vec3Sub(b, a)
	s2 = vec3Sub(c, a)
	c = vec3Normalize(vec3Cross(s2, s1))
	d = vec3Dot(c, a)
	return Vec4(c.x, c.y, c.z, d)

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
			a = Vec3(float(tokens[1]), float(tokens[2]), float(tokens[3]))
			b = Vec3(float(tokens[6]), float(tokens[7]), float(tokens[8]))
			c = Vec3(float(tokens[11]), float(tokens[12]), float(tokens[13]))
			mapBrushFace.plane = planeFromPoints(a, b, c)
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

# search the list and return the first entity with the given classname
def findByClassName(mapEntities, className):
	for mapEntity in mapEntities:
		if mapEntity["classname"] == className:
			return mapEntity
	return None

# search the list and return the first entity with the given targetname
def findByTargetName(mapEntities, targetName):
	for mapEntity in mapEntities:
		if "targetname" in mapEntity and mapEntity["targetname"] == targetName:
			return mapEntity
	return None

# parse entity origin into vec3
def getEntityFieldVec3(mapEntity, field):
	tokens = mapEntity[field].split()
	return Vec3(float(tokens[0]), float(tokens[1]), float(tokens[2]))

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

	# write out ini
	iniFile = open(sys.argv[3], "w")
	if "render_width" in mapEntities[0]:
		iniFile.write(f"+W{mapEntities[0]["render_width"]}\n")
	if "render_height" in mapEntities[0]:
		iniFile.write(f"+H{mapEntities[0]["render_height"]}\n")
	iniFile.write(f"Input_File_Name={sys.argv[2]}\n")
	iniFile.close()

	# get camera
	mapCamera = findByClassName(mapEntities, "pov_camera")
	if mapCamera == None:
		die("Map has no pov_camera entity!")

	# get target
	mapCameraLookAt = None
	if "target" in mapCamera:
		mapCameraTarget = findByTargetName(mapEntities, mapCamera["target"])
		if mapCameraTarget != None:
			mapCameraLookAt = getEntityFieldVec3(mapCameraTarget, "origin")
		else:
			print("WARNING: Camera target specified does not exist!")

	# write out pov
	povFile = open(sys.argv[2], "w")

	# write camera
	povFile.write("camera {\n")
	povFile.write("\tsky <0, 0, 1>\n")
	povFile.write("\tdirection <-1, 0, 0>\n")
	mapCameraOrigin = getEntityFieldVec3(mapCamera, "origin")
	povFile.write(f"\tlocation <{mapCameraOrigin.x}, {mapCameraOrigin.y}, {mapCameraOrigin.z}>\n")
	if mapCameraLookAt != None:
		povFile.write(f"\tlook_at <{mapCameraLookAt.x}, {mapCameraLookAt.y}, {mapCameraLookAt.z}>\n")
	if "fov" in mapCamera:
		povFile.write(f"\tangle {float(mapCamera["fov"])}\n")
	povFile.write("}\n\n")

	# write lights
	for mapEntity in mapEntities:
		if mapEntity["classname"] == "pov_light":
			origin = getEntityFieldVec3(mapEntity, "origin")
			povFile.write("light_source {\n")
			povFile.write(f"\t<{origin.x}, {origin.y}, {origin.z}>\n")
			povFile.write("\tcolor rgb <1, 1, 1>\n")
			povFile.write("}\n\n")

	# write solids
	for mapEntity in mapEntities:
		for mapBrush in mapEntity.brushes:
			povFile.write("intersection {\n")
			for mapBrushFace in mapBrush.faces:
				povFile.write(f"\tplane {{<{mapBrushFace.plane.x}, {mapBrushFace.plane.y}, {mapBrushFace.plane.z}>, {mapBrushFace.plane.w}}}\n")
			povFile.write("\tpigment { rgb <1, 0, 1> }\n}\n\n")

	# clean up
	povFile.close()
