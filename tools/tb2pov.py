#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math
from PIL import Image

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
	if field not in mapEntity:
		return Vec3(0, 0, 0)
	tokens = mapEntity[field].split()
	return Vec3(float(tokens[0]), float(tokens[1]), float(tokens[2]))

# write generic key
def writeIniKey(iniFile, mapEntity, entityKeyname, iniKeyName):
	if entityKeyname in mapEntity:
		iniFile.write(f"{iniKeyName}={mapEntity[entityKeyname]}\n")

# write boolean key
def writeIniBoolKey(iniFile, mapEntity, entityKeyname, iniKeyName):
	if entityKeyname in mapEntity:
		if int(mapEntity[entityKeyname]):
			iniFile.write(f"{iniKeyName}=On\n")
		else:
			iniFile.write(f"{iniKeyName}=Off\n")

# start here
if __name__ == "__main__":

	if len(sys.argv) != 4:
		printHelp()

	inputFile = open(sys.argv[1], "r")
	if not inputFile:
		die(f"Failed to open {sys.argv[1]}")

	# parse map structure
	mapEntities = parseMapEntities(inputFile)

	# write out ini
	iniFile = open(sys.argv[3], "w")
	writeIniBoolKey(iniFile, mapEntities[0], "bounding", "Bounding")
	writeIniBoolKey(iniFile, mapEntities[0], "display", "Display")
	writeIniBoolKey(iniFile, mapEntities[0], "render_alpha", "Output_Alpha")
	writeIniBoolKey(iniFile, mapEntities[0], "verbose", "Verbose")
	writeIniBoolKey(iniFile, mapEntities[0], "antialias", "Antialias")
	writeIniBoolKey(iniFile, mapEntities[0], "jitter", "Jitter")
	writeIniBoolKey(iniFile, mapEntities[0], "sampling_method", "Sampling_Method")
	writeIniKey(iniFile, mapEntities[0], "render_width", "Width")
	writeIniKey(iniFile, mapEntities[0], "render_height", "Height")
	writeIniKey(iniFile, mapEntities[0], "quality", "Quality")
	writeIniKey(iniFile, mapEntities[0], "bounding_threshold", "Bounding_Threshold")
	writeIniKey(iniFile, mapEntities[0], "antialias_threshold", "Antialias_Threshold")
	writeIniKey(iniFile, mapEntities[0], "antialias_depth", "Antialias_Depth")
	writeIniKey(iniFile, mapEntities[0], "jitter_amount", "Jitter_Amount")
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
	povFile.write("#version 3.7;\n\n")

	# if there's a logo in the scene, write the necessary stuff
	if findByClassName(mapEntities, "pov_logo") != None:
		povFile.write("#include \"logo.inc\"\n\n")
		povFile.write("#declare LogoPigment =\n")
		povFile.write("pigment {\n")
		povFile.write("\tplanar scale 2 translate y\n")
		povFile.write("\tcolor_map {\n")
		povFile.write("\t\t[0.0, color <1.0, 0.4, 0.4>*0.7]\n")
		povFile.write("\t\t[0.5, color <0.4, 0.9, 0.4>*0.7]\n")
		povFile.write("\t\t[1.0, color <0.4, 0.4, 1.0>*0.7]\n")
		povFile.write("\t}\n")
		povFile.write("}\n\n")

	# write global settings
	povFile.write("global_settings {\n")
	if "assumed_gamma" in mapEntities[0]:
		povFile.write(f"\tassumed_gamma {mapEntities[0]["assumed_gamma"]}\n")
	else:
		povFile.write("\tassumed_gamma 1.0\n")
	if "ambient_light" in mapEntities[0]:
		ambient_light = getEntityFieldVec3(mapEntities[0], "ambient_light")
		povFile.write(f"\tambient_light <{ambient_light.x}, {ambient_light.y}, {ambient_light.z}>\n")
	povFile.write("}\n\n")

	# write background
	povFile.write("background {\n")
	if "background" in mapEntities[0]:
		background = getEntityFieldVec3(mapEntities[0], "background")
		if "background_alpha" in mapEntities[0]:
			povFile.write(f"\tcolor rgbt <{background.x}, {background.y}, {background.z}, {1.0 - float(mapEntities[0]["background_alpha"])}>\n")
		else:
			povFile.write(f"\tcolor rgb <{background.x}, {background.y}, {background.z}>\n")
	elif "background_alpha" in mapEntities[0]:
		povFile.write(f"\tcolor rgbt <0.0, 0.0, 0.0, {1.0 - float(mapEntities[0]["background_alpha"])}>\n")
	povFile.write("}\n\n")

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

	# write fog
	mapFog = findByClassName(mapEntities, "pov_fog")
	if mapFog != None:
		povFile.write("fog {\n")
		if "fog_type" in mapFog:
			povFile.write(f"\tfog_type {mapFog["fog_type"]}\n")
		if "distance" in mapFog:
			povFile.write(f"\tdistance {mapFog["distance"]}\n")
		if "lambda" in mapFog:
			povFile.write(f"\tlambda {mapFog["lambda"]}\n")
		if "fog_offset" in mapFog:
			povFile.write(f"\tfog_offset {mapFog["fog_offset"]}\n")
		if "fog_alt" in mapFog:
			povFile.write(f"\tfog_alt {mapFog["fog_alt"]}\n")
		if "octaves" in mapFog:
			povFile.write(f"\toctaves {mapFog["octaves"]}\n")
		if "omega" in mapFog:
			povFile.write(f"\tomega {mapFog["omega"]}\n")
		if "turb_depth" in mapFog:
			povFile.write(f"\turb_depth {mapFog["turb_depth"]}\n")
		if "turbulence" in mapFog:
			turbulence = getEntityFieldVec3(mapFog, "turbulence")
			povFile.write(f"\tturbulence <{turbulence.x}, {turbulence.y}, {turbulence.z}>\n")
		if "up" in mapFog:
			up = getEntityFieldVec3(mapFog, "up")
			povFile.write(f"\tup <{up.x}, {up.y}, {up.z}>\n")
		if "color" in mapFog:
			color = getEntityFieldVec3(mapFog, "color")
			povFile.write(f"\tcolor rgb <{color.x}, {color.y}, {color.z}>\n")
		povFile.write("}\n\n")

	# write objects
	for mapEntity in mapEntities:
		origin = getEntityFieldVec3(mapEntity, "origin")
		if mapEntity["classname"] == "pov_light":
			povFile.write("light_source {\n")
			povFile.write(f"\t<{origin.x}, {origin.y}, {origin.z}>\n")
			if "color" in mapEntity:
				color = getEntityFieldVec3(mapEntity, "color")
				if "scale" in mapEntity:
					povFile.write(f"\tcolor rgb <{color.x}, {color.y}, {color.z}> * {float(mapEntity["scale"])}\n")
				else:
					povFile.write(f"\tcolor rgb <{color.x}, {color.y}, {color.z}>\n")
			else:
				if "scale" in mapEntity:
					povFile.write(f"\tcolor rgb <1, 1, 1> * {float(mapEntity["scale"])}\n")
				else:
					povFile.write("\tcolor rgb <1, 1, 1>\n")
			povFile.write("}\n\n")
		elif mapEntity["classname"] == "pov_logo":
			povFile.write("object {\n")
			povFile.write("\tPovray_Logo\n")
			povFile.write("\tpigment { LogoPigment }\n")
			povFile.write("\trotate 90*x\n")
			povFile.write("\trotate 90*z\n")
			if "angles" in mapEntity:
				angles = getEntityFieldVec3(mapEntity, "angles")
				povFile.write(f"\trotate <{angles.z}, {angles.x}, {angles.y}>\n")
			if "scale" in mapEntity:
				povFile.write(f"\tscale {128 * float(mapEntity["scale"])}\n")
			else:
				povFile.write("\tscale 128\n")
			povFile.write(f"\ttranslate <{origin.x}, {origin.y}, {origin.z}>\n")
			povFile.write("}\n\n")

	# write solids
	for mapEntity in mapEntities:
		for mapBrush in mapEntity.brushes:
			povFile.write("intersection {\n")
			for mapBrushFace in mapBrush.faces:
				im = Image.open(f"{mapBrushFace.texture}.png")
				povFile.write(f"\tplane {{<{mapBrushFace.plane.x}, {mapBrushFace.plane.y}, {mapBrushFace.plane.z}>, {mapBrushFace.plane.w}")
				povFile.write(f" texture {{ scale <{im.size[0] * mapBrushFace.scale.x}, {im.size[1] * mapBrushFace.scale.y}, 1> matrix <{mapBrushFace.u.x}, {mapBrushFace.u.y}, {mapBrushFace.u.z}, {-mapBrushFace.v.x}, {-mapBrushFace.v.y}, {-mapBrushFace.v.z}, {mapBrushFace.plane.x}, {mapBrushFace.plane.y}, {mapBrushFace.plane.z}, {mapBrushFace.u.w}, {mapBrushFace.v.w}, {mapBrushFace.plane.w}> pigment {{ image_map {{ png \"{mapBrushFace.texture}.png\" }} }} }} }}\n")
			povFile.write("}\n\n")

	# clean up
	povFile.close()
