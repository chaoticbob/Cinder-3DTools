"""
 Copyright 2016 Google Inc.
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
 http://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.


 Copyright (c) 2016, The Cinder Project, All rights reserved.

 This code is intended for use with the Cinder C++ library: http://libcinder.org

 Redistribution and use in source and binary forms, with or without modification, are permitted provided that
 the following conditions are met:

	* Redistributions of source code must retain the above copyright notice, this list of conditions and
	the following disclaimer.
	* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and
	the following disclaimer in the documentation and/or other materials provided with the distribution.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
 WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
 PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
 ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
 TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 POSSIBILITY OF SUCH DAMAGE.
"""

#
# import sys
# sys.path.append( "C:/Users/hai/code/cinder/Cinder-3DTools/Maya/TriMeshExporter" )
# import TriMeshExporter
# reload( TriMeshExporter )
# 
# b = TriMeshExporter.TriMeshExporter()
# b.exportSelected( "C:/Users/hai/code/temp/maya", "mydata" )
#

import maya.api.OpenMaya as OpenMaya
import array
import math 
import xml.dom.minidom as minidom
import os
import re
import struct
import xml.etree.cElementTree as ET

## TriMesh
#
# This class is generic. Should be usable outside of Maya.
#
class TriMesh( object ):
	POSITION    = 0x00000001
	COLOR       = 0x00000002
	TEX_COORD_0 = 0x00000004
	TEX_COORD_1 = 0x00000008
	TEX_COORD_2 = 0x00000010
	TEX_COORD_3 = 0x00000020
	NORMAL      = 0x00000100
	TANGENT     = 0x00000200
	BITANGENT   = 0x00000400
	BONE_INDEX  = 0x00001000
	BONE_WEIGHT = 0x00002000
	CUSTOM_0    = 0x00010000
	CUSTOM_1    = 0x00020000
	CUSTOM_2    = 0x00040000
	CUSTOM_3    = 0x00080000
	CUSTOM_4    = 0x00100000
	CUSTOM_5    = 0x00200000
	CUSTOM_6    = 0x00400000
	CUSTOM_7    = 0x00800000
	CUSTOM_8    = 0x01000000
	CUSTOM_9    = 0x02000000	

	def __init__( self ):
		self.version    = int(2)
		self.indices    = array.array( 'L' )
		self.positions  = array.array( 'f' )
		self.colors     = array.array( 'f' )
		self.normals    = array.array( 'f' )
		self.texCoords0 = array.array( 'f' )
		self.texCoords1 = array.array( 'f' )
		self.texCoords2 = array.array( 'f' )
		self.texCoords3 = array.array( 'f' )
		self.tangents   = array.array( 'f' )
		self.bitangents = array.array( 'f' )

		self.positionsDims  = 0
		self.colorsDims     = 0
		self.normalsDims    = 0
		self.texCoords0Dims = 0
		self.texCoords1Dims = 0
		self.texCoords2Dims = 0
		self.texCoords3Dims = 0
		self.tangentsDims   = 0
		self.bitangentsDims = 0		
		pass

	def appendPosition( self, x, y, z = None, w = None ):
		self.positions.append( x )
		self.positions.append( y )
		if z is not None:
			self.positions.append( z )
		if w is not None:
			self.positions.append( w )
		if 0 == self.positionsDims:
			if w is not None:
				self.positionsDims = 4
			elif z is not None:
				self.positionsDims = 3
			else:
				self.positionsDims = 2
		pass

	def appendNormal( self, x, y, z ):
		self.normals.append( x )
		self.normals.append( y )
		self.normals.append( z )
		if 0 == self.normalsDims:
			self.normalsDims = 3
		pass

	def appendTangent( self, x, y, z ):
		self.tangents.append( x )
		self.tangents.append( y )
		self.tangents.append( z )
		if 0 == self.tangentsDims:
			self.tangentsDims = 3
		pass

	def appendBitangent( self, x, y, z ):
		self.bitangents.append( x )
		self.bitangents.append( y )
		self.bitangents.append( z )
		if 0 == self.bitangentsDims:
			self.bitangentsDims = 3
		pass

	def appendRgb( self, r, g, b ):
		self.colors.append( r )
		self.colors.append( g )
		self.colors.append( b )
		if 0 == self.colorsDims:
			self.colorsDims = 3
		pass

	def appendRgba( self, r, g, b, a ):
		self.colors.append( r )
		self.colors.append( g )
		self.colors.append( b )
		self.colors.append( a )
		if 0 == self.colorsDims:
			self.colorsDims = 4
		pass

	def appendTexCoord0( self, x, y, z = None, w = None ):
		self.texCoords0.append( x )
		self.texCoords0.append( y )
		if z is not None:
			self.texCoords0.append( z )
		if w is not None:
			self.texCoords0.append( w )
		if 0 == self.texCoords0Dims:
			if w is not None:
				self.texCoords0Dims = 4
			elif z is not None:
				self.texCoords0Dims = 3
			else:
				self.texCoords0Dims = 2			
		pass

	def appendTexCoord1( self, x, y, z = None, w = None ):
		self.texCoords1.append( x )
		self.texCoords1.append( y )
		if z is not None:
			self.texCoords1.append( z )
		if w is not None:
			self.texCoords1.append( w )
		if 0 == self.texCoords1Dims:
			if w is not None:
				self.texCoords1Dims = 4
			elif z is not None:
				self.texCoords1Dims = 3
			else:
				self.texCoords1Dims = 2
		pass

	def appendTexCoord2( self, x, y, z = None, w = None ):
		self.texCoords2.append( x )
		self.texCoords2.append( y )
		if z is not None:
			self.texCoords2.append( z )
		if w is not None:
			self.texCoords2.append( w )
		if 0 == self.texCoords2Dims:
			if w is not None:
				self.texCoords2Dims = 4
			elif z is not None:
				self.texCoords2Dims = 3
			else:
				self.texCoords2Dims = 2			
		pass

	def appendTexCoord3( self, x, y, z = None, w = None ):
		self.texCoords3.append( x )
		self.texCoords3.append( y )
		if z is not None:
			self.texCoords3.append( z )
		if w is not None:
			self.texCoords3.append( w )
		if 0 == self.texCoords3Dims:
			if w is not None:
				self.texCoords3Dims = 4
			elif z is not None:
				self.texCoords3Dims = 3
			else:
				self.texCoords3Dims = 2					
		pass

	def appendIndex( self, v ):
		self.indices.append( v )
		pass		

	def appendTriangle( self, v0, v1, v2 ):
		self.indices.append( v0 )
		self.indices.append( v1 )
		self.indices.append( v2 )
		pass

	def getNumVertices( self ):
		return len( self.indices )
		pass

	def writeAttrib( self, file, attrib, dims, size, data ):
		if 0 == size:
			return
		file.write( struct.pack( "I", attrib ) )
		file.write( struct.pack( "B", dims ) )
		file.write( struct.pack( "I", size ) )
		data.tofile( file )
		pass

	def write( self, path ):
		try:
			file = open( path, "wb" )
		except:
			print( "Failed to open file for write: %s" % path )
			return
		file.write( struct.pack( "B", self.version ) )
		file.write( struct.pack( "I", self.getNumVertices() ) )
		# Write indices
		if self.getNumVertices() > 0:
			self.indices.tofile( file )
		# Write attributes
		print( self.positions )
		self.writeAttrib( file, TriMesh.POSITION, self.positionsDims, len( self.positions ), self.positions )
		self.writeAttrib( file, TriMesh.COLOR, self.colorsDims, len( self.colors ), self.colors )
		self.writeAttrib( file, TriMesh.NORMAL, self.normalsDims, len( self.normals ), self.normals )
		self.writeAttrib( file, TriMesh.TEX_COORD_0, self.texCoords0Dims, len( self.texCoords0 ), self.texCoords0 )
		self.writeAttrib( file, TriMesh.TEX_COORD_1, self.texCoords1Dims, len( self.texCoords1 ), self.texCoords1 )
		self.writeAttrib( file, TriMesh.TEX_COORD_2, self.texCoords2Dims, len( self.texCoords2 ), self.texCoords2 )
		self.writeAttrib( file, TriMesh.TEX_COORD_3, self.texCoords3Dims, len( self.texCoords3 ), self.texCoords3 )
		self.writeAttrib( file, TriMesh.TANGENT, self.tangentsDims, len( self.tangents ), self.tangents )
		self.writeAttrib( file, TriMesh.BITANGENT,  self.bitangentsDims, len( self.bitangents ), self.bitangents )
		file.close()
		pass

	# class TriMesh
	pass

## MeshInfo
class MeshInfo( object ):
	## c'tor
	def __init__( self, transformDagPath = None, shapeDagPath = None ):
		self.transformDagPath = transformDagPath
		self.shapeDagPath = shapeDagPath
		pass

	## isValid
	def isValid( self ):
		return True if ( ( self.transformDagPath is not None ) and ( self.shapeDagPath is not None ) ) else False
		pass

	## partialPathName
	def partialPathName( self ):
		return self.transformDagPath.partialPathName() if self.transformDagPath is not None else None
		pass		
	pass

## TriMeshExporter
class TriMeshExporter( object ):
	## c'tor
	def __init__( self ):
		self.basePath = None
		pass

	## createFilePath
	def createFilePath( self, parentDagPath, dagPath, instanceCount, path, shaderTag, ext ):
		# Use parent node name if the current node is not instanced
		fileName = parentDagPath.partialPathName()
		if instanceCount > 1:
			fileName = dagPath.partialPathName()
		# Remove the first instance of | 
		if fileName.startswith( "|" ):
			fileName = re.sub( "\|", "", fileName, count = 1 )
		# Replace all remaining instances of | with _
		fileName = re.sub( "\|", "_", fileName )
		# Add shaderTag
		if shaderTag:
			fileName = "%s_%s" % ( fileName, shaderTag )
		# Create full path
		if ext.startswith( "." ):
			fileName = os.path.join( path, fileName ) + ext	
		else: 			
			fileName = os.path.join( path, fileName ) + "." + ext	
		# Return it!
		return fileName
		pass		

	## createFilePath
	def getShaderNode( self, shaderObj ):
		sgNode = OpenMaya.MFnDependencyNode( shaderObj )
		# Get surfaceShader plug in shading group node
		dstPlug = sgNode.findPlug( "surfaceShader", False )
		# Find plug surface shader
		srcPlugs = dstPlug.connectedTo( True, False )
		# Shader node
		shaderNode = OpenMaya.MFnDependencyNode( srcPlugs[0].node() )
		# Return shader node
		return shaderNode
		pass

	## createFilePath
	def getColor( self, shaderNode ):
		result = [[0.0, 0.0, 0.0], None]
		# Get color plug
		dstColorPlug = shaderNode.findPlug( "color", False )
		# Texture or color
		if dstColorPlug.isConnected:
			srcColorPlugs = dstColorPlug.connectedTo( True, False )
			srcColorNode = OpenMaya.MFnDependencyNode( srcColorPlugs[0].node() )
			if "file" == srcColorNode.typeName:
				fileNamePlug = srcColorNode.findPlug( "fileTextureName", False )
				fileName = fileNamePlug.asString()
				fileName = os.path.relpath( fileName, self.basePath )
				result[1] = fileName
		else:
			colorR = shaderNode.findPlug( "colorR", False )
			colorG = shaderNode.findPlug( "colorG", False )
			colorB = shaderNode.findPlug( "colorB", False )
			result[0][0] = colorR.asFloat()
			result[0][1] = colorG.asFloat()
			result[0][2] = colorB.asFloat()
		# Return
		return result
		pass

	## createFilePath
	def createTriMesh( self, mesh, meshData, polyFaces, colorRgb ):
		points    = meshData["position"]
		normals   = meshData["normal"]
		texCoord0 = meshData["texCoord0"]
		# TriMesh
		triMesh = TriMesh()
		# Indices
		for face in polyFaces:
			vertices = mesh.getPolygonVertices( face )
			for vertex in vertices:
				triMesh.appendIndex( vertex )
		# Positions and color
		for P in points:
			triMesh.appendPosition( P.x, P.y, P.z )
			triMesh.appendRgb( colorRgb[0], colorRgb[1], colorRgb[2] )
		# Normals
		for N in normals:
			triMesh.appendPosition( N.x, N.y, N.z )
		# TexCoords0
		for uv in texCoord0:
			triMesh.appendPosition( uv.x, uv.y )
		return triMesh
		pass

	## createFilePath
	def writeTriMeshFile( self, parentDagPath, xmlParent, path, mesh, meshData, shaderCount, shaderObj, polyFaces ):
		if not mesh:
			return
		# Get DAG path
		dagPath = mesh.dagPath()
		# Get shader node
		try:
			shaderNode = self.getShaderNode( shaderObj )
		except:
			print( "Couldn't get surfaceShader node for %s" % dagPath.partialPathName() )
			return			
		# Get color
		try:
			[colorRgb, colorFile] = self.getColor( shaderNode )
		except:
			print( "Couldn't get color for %s" % dagPath.partialPathName() )
			return
		# Write initial data to XML
		xml = ET.SubElement( xmlParent, "shaderSet", name = shaderNode.name() )
		if None != colorFile:
			xml.set( "surfaceShaderColorFile", colorFile )
		# Get buffers
		triMesh = self.createTriMesh( mesh, meshData, polyFaces, colorRgb )
		# Write buffers
		geoXml = ET.SubElement( xml, "geometry" )
		geoXml.set( "vertexCount", str( triMesh.getNumVertices() ) ) 
		# Generate file path
		shaderTag = shaderNode.name() if shaderCount > 1 else None
		filePath = self.createFilePath( parentDagPath, dagPath, mesh.instanceCount( False ), path, shaderTag, ".mesh" );
		triMesh.write( filePath )
		# Add triMeshFile attribute
		relFilePath = os.path.relpath( filePath, self.basePath )
		geoXml.set( "triMeshFile", relFilePath )
		# Write out data
		print( "Exported %s to %s" % ( dagPath.partialPathName(), filePath ) )		
		pass


	def getMeshData( self, mesh ):
		print( mesh.getTriangles() )

		[meshTriCounts, meshTriVertices] = mesh.getTriangles()
		faceTrianglesVertices = []
		vertexOffset = 0
		for polyIdx in range( 0, len( meshTriCounts ) ):
			vertexCount = 3 * meshTriCounts[polyIdx]
			trianglesVerticess = array.array( "I" )
			for vertexIdx in range( vertexOffset, vertexOffset + vertexCount ):
				trianglesVerticess.append( meshTriVertices[vertexIdx] )
				pass
			faceTrianglesVertices.append( trianglesVerticess )
			pass

		print( faceTrianglesVertices )

		meshData = {}
		meshData["position"]  = mesh.getFloatPoints()
		meshData["normal"]    = mesh.getVertexNormals( False )
		meshData["tangent"]   = mesh.getTangents
		meshData["texCoord0"] = OpenMaya.MFloatPointArray()
		[uArray, vArray] = mesh.getUVs()
		for i in range( 0, len( uArray ) ):
			meshData["texCoord0"].append( OpenMaya.MFloatPoint( uArray[i], vArray[i] ) )		
			pass
		return meshData
		pass

	def getShaderFaces( self, mesh, instance ):
		shaderFaces = {}
		[shaderObjs, polyInfos] = mesh.getConnectedShaders( instance )
		for polyIdx in range( 0, mesh.numPolygons ):
			shaderObjIdx = polyInfos[polyIdx]
			if shaderObjIdx in shaderFaces:
				shaderFaces[shaderObjIdx].append( polyIdx )
			else:
				shaderFaces[shaderObjIdx] = []
				shaderFaces[shaderObjIdx].append( polyIdx )
			pass
		return shaderFaces
		pass

	## createFilePath
	def exportMesh(self, transformDagPath, shapeDagPath, path, xmlParent):
		if OpenMaya.MFn.kMesh != shapeDagPath.apiType():
			print( "Node isn't MFnMesh : %s" % shapeDagPath.partialPathName())
			return
		# Create mesh XML node
		xml = ET.SubElement(xmlParent, "mesh", name = shapeDagPath.partialPathName())
		# Transform data
		transform = OpenMaya.MFnTransform( transformDagPath )
		matrix = transform.transformation().asMatrix()
		elements = []
		for row in range( 0, 4 ):
			for col in range( 0, 4 ):
				value = matrix.getElement( row, col )
				elements.append( float( value ) )
		xml.set( "transform", " ".join( map( str, elements ) ) )
		# Get mesh data
		mesh = OpenMaya.MFnMesh(shapeDagPath)
		meshData = self.getMeshData( mesh )
		# Get connected shaders
		instance = 0
		shaderFaces = self.getShaderFaces( mesh, instance )
		# Write TriMesh file
		shaderCount = len( shaderFaces )
		for shaderObjIdx in shaderFaces:
			shaderObj = shaderObjs[shaderObjIdx]
			polyFaces = shaderFaces[shaderObjIdx]
			self.writeTriMeshFile( transformDagPath, xml, path, mesh, meshData, shaderCount, shaderObj, polyFaces )
			pass
		pass

	## findMayaMeshes
	def findMayaMeshes( self, dagPath ):
		result = []
		for childNum in range( 0, dagPath.childCount() ):
			childObj = dagPath.child( childNum )
			childDagPath = OpenMaya.MDagPath.getAPathTo( childObj )
			childApiType = childDagPath.apiType()
			if OpenMaya.MFn.kTransform == childApiType:
				meshInfos = self.findMayaMeshes( childDagPath )
				result.extend( meshInfos )
			elif OpenMaya.MFn.kMesh == childApiType:
				mi = MeshInfo( dagPath, childDagPath )
				result.append( mi )
				pass
			pass
		return result
		pass		

	## createFilePath
	def exportSelected( self, path, xmlName ):
		self.basePath = path
		selList = OpenMaya.MGlobal.getActiveSelectionList()
		if selList.isEmpty():
			print( "Nothing selected" )
			return
		print( "Exporting as Cinder TriMesh data to %s" % path )
		if not os.path.exists( path ):
			os.makedirs( path )
		# Create XML doc
		xmlRoot = ET.Element( "data" )
		# Find all mesh shape nodes and their immediate transforms
		meshInfos = []
		it = OpenMaya.MItSelectionList( selList );
		while not it.isDone():
			#self.exportDagPath( xmlRoot, it.getDagPath(), path, fileName );
			tmpMeshInfos = self.findMayaMeshes( it.getDagPath() )
			meshInfos.extend( tmpMeshInfos )
			# Advance to next item
			it.next()
		pass
		# Export mesh geometry
		for meshInfo in meshInfos:
			self.exportMesh( meshInfo.transformDagPath, meshInfo.shapeDagPath, path, xmlRoot )
		# Write XML
		if len( list( xmlRoot ) ) > 0:
			tree = ET.ElementTree( xmlRoot )
			prettyXml = minidom.parseString( ET.tostring( xmlRoot ) ).toprettyxml( indent="   " )
			file = open( os.path.join( path, xmlName + ".xml" ), "w" )
			file.write( prettyXml )	

	pass
