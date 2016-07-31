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
# sys.path.append( "C:/Users/hai/code/cinder/Cinder-3DTools/Cinder-3DTools/Maya/TriMeshExporter" )
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
		self.position.append( x )
		self.position.append( y )
		if z is not None:
			self.position.append( z )
		if w is not None:
			self.position.append( w )
		if 0 == self.positionsDims:
			if w is not None:
				self.positionDims = 4
			elif z is not None:
				self.positionDims = 3
			else:
				self.positionDims = 2
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
		if 0 == len( data ):
			return
		file.write( struct.pack( 'I', attrib ) )
		file.write( struct.pack( 'b', dim ) )
		file.write( struct.pack( 'I', size ) )
		data.tofile( file )
		pass

	def write( self, path ):
		file = open( path, "wb" )
		file.write( struct.pack( 'I', self.version ) )
		file.write( struct.pack( 'I', self.getNumVertices() ) )
		if self.getNumVertices() > 0:
			self.indices.tofile( file )
		self.writeAttrib( file, TriMesh.POSITION, self.positionsDims, len( self.positions ), self.positions )
		self.writeAttrib( file, TriMesh.COLOR, self.colorsDims, len( self.colors ), self.colors )
		self.writeAttrib( file, TriMesh.TEX_COORD_0, self.texCoords0Dims, len( self.texCoords0 ), self.texCoords0 )
		self.writeAttrib( file, TriMesh.TEX_COORD_1, self.texCoords1Dims, len( self.texCoords1 ), self.texCoords1 )
		self.writeAttrib( file, TriMesh.TEX_COORD_2, self.texCoords2Dims, len( self.texCoords2 ), self.texCoords2 )
		self.writeAttrib( file, TriMesh.TEX_COORD_3, self.texCoords3Dims, len( self.texCoords3 ), self.texCoords3 )
		self.writeAttrib( file, TriMesh.NORMAL, self.normalsDims, len( self.normals ), self.normals )
		self.writeAttrib( file, TriMesh.TANGENT, self.tangentsDims, len( self.tangents ), self.tangents )
		self.writeAttrib( file, TriMesh.BITANGENT,  self.bitangentsDims, len( self.bitangents ), self.bitangents )
		file.close()
		pass

	# class TriMesh
	pass


## TriMeshExporter
class TriMeshExporter( object ):
	## c'tor
	def __init__( self ):
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
				fileName = srcColorNode.findPlug( "fileTextureName", False )
				result[1] = fileName.asString()
		else:
			colorR = shaderNode.findPlug( "colorR", False )
			colorG = shaderNode.findPlug( "colorG", False )
			colorB = shaderNode.findPlug( "colorB", False )
			result[0][0] = colorR.asFloat()
			result[0][1] = colorR.asFloat()
			result[0][2] = colorR.asFloat()
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
		# Write out data
		print( "Exported %s to %s" % ( dagPath.partialPathName(), filePath ) )		
		pass

	## createFilePath
	def exportMesh( self, transformDagPath, dagPath, path, xmlParent ):
		if OpenMaya.MFn.kMesh != dagPath.apiType():
			print( "Node isn't MFnMesh : %s" % dagPath.partialPathName() )
			return

		xml = ET.SubElement( xmlParent, "mesh", name = dagPath.partialPathName() )

		mesh = OpenMaya.MFnMesh( dagPath )
		meshData = {}
		meshData["position"]  = mesh.getFloatPoints()
		meshData["normal"]    = mesh.getVertexNormals( False )
		meshData["texCoord0"] = mesh.getUVs()
		meshData["tangent"]   = mesh.getTangents

		instance = 0
		[shaderObjs, polyInfos] = mesh.getConnectedShaders( instance )
		
		shaderFaces = {}
		for polyIdx in range( 0, mesh.numPolygons ):
			shaderObjIdx = polyInfos[polyIdx]
			if shaderObjIdx in shaderFaces:
				shaderFaces[shaderObjIdx].append( polyIdx )
			else:
				shaderFaces[shaderObjIdx] = []
				shaderFaces[shaderObjIdx].append( polyIdx )

		shaderCount = len( shaderFaces )
		for shaderObjIdx in shaderFaces:
			shaderObj = shaderObjs[shaderObjIdx]
			polyFaces = shaderFaces[shaderObjIdx]
			self.writeTriMeshFile( transformDagPath, xml, path, mesh, meshData, shaderCount, shaderObj, polyFaces )			
		pass

	## createFilePath
	def exportDagPath( self, xmlRoot, dagPath, path, fileName ):
		apiType = dagPath.apiType()
		if OpenMaya.MFn.kTransform == apiType:
			numShapes = dagPath.numberOfShapesDirectlyBelow()
			for i in range( 0, numShapes ):
				shapeDagPath = OpenMaya.MDagPath( dagPath )
				shapeDagPath.extendToShape( i )
				if OpenMaya.MFn.kMesh == shapeDagPath.apiType():
					self.exportMesh( dagPath, shapeDagPath, path, xmlRoot )
				else:
					print( "Unsupported node (apiType=%d) : %s" % ( shapeDagPath.apiType(), shapeDagPath.partialPathName() ) )					
		elif OpenMaya.MFn.kMesh == apiType:
			self.exportMesh( None, dagPath, path, xmlRoot )			
		else:
			print( "Unsupported node (apiType=%d) : %s" % ( dagPath.apiType(), dagPath.partialPathName() ) )
		pass

	## createFilePath
	def exportSelected( self, path, fileName ):
		selList = OpenMaya.MGlobal.getActiveSelectionList()
		if selList.isEmpty():
			print( "Nothing selected" )
			return

		print( "Exporting as Cinder TriMesh data to %s" % path )
		if not os.path.exists( path ):
			os.makedirs( path )

		xmlRoot = ET.Element( "data" )

		it = OpenMaya.MItSelectionList( selList );
		while not it.isDone():
			#mesh = OpenMaya.MFnMesh( it.getDagPath() )
			self.exportDagPath( xmlRoot, it.getDagPath(), path, fileName );
			it.next()
		pass

		if len( list( xmlRoot ) ) > 0:
			tree = ET.ElementTree( xmlRoot )
			prettyXml = minidom.parseString( ET.tostring( xmlRoot ) ).toprettyxml( indent="   " )
			file = open( os.path.join( path, fileName + ".xml" ), "w" )
			file.write( prettyXml )	

	pass
