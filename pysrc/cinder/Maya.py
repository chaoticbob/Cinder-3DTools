
from Base import BaseMaterial, BaseMesh, BaseExporter
from TriMesh import TriMesh

import maya.api.OpenMaya as OpenMaya
import maya.OpenMaya as OpenMaya_v1
import maya.cmds as cmds

## \class MayaMaterial
class MayaMaterial( BaseMaterial ):
	## c'tor
	def __init__( self ):
		print( "BaseMaterial c'tor" )		
		pass

	## class BaseMaterial
	pass

## \class MayaMesh
#
#
class MayaMesh( BaseMesh ):
	## c'tor
	def __init__( self, transformDagPath, shapeDagPath ):
		super( MayaMesh, self ).__init__()
		print( "MayaMesh c'tor" )
		self.transformDagPath = transformDagPath
		self.shapeDagPath = shapeDagPath
		pass

	## getName
	def getName( self ):
		return self.transformDagPath.partialPathName() if self.transformDagPath is not None else None
		pass

	## getTriMesh
	def getTriMeshes( self ):
		result = {}
		return result		
		pass

	# class MayaMesh		
	pass		

## \class
#
#
class MayaExporter( BaseExporter ):
	## c'tor
	def __init__( self ):
		super( MayaExporter, self ).__init__()
		print( "MayaExporter c'tor" )
		pass

	## findMayaMeshes
	def findMayaMeshes( self, dagPath, existingMeshes ):
		result = []
		for childNum in range( 0, dagPath.childCount() ):
			childObj = dagPath.child( childNum )
			childDagPath = OpenMaya.MDagPath.getAPathTo( childObj )
			childApiType = childDagPath.apiType()
			if OpenMaya.MFn.kTransform == childApiType:
				meshInfos = self.findMayaMeshes( childDagPath, existingMeshes )
				result.extend( meshInfos )
			elif OpenMaya.MFn.kMesh == childApiType:
				mi = MayaMesh( dagPath, childDagPath )
				append = True
				# Filter so we have unique paths
				for exMi in existingMeshes:
					if ( mi.transformDagPath == exMi.transformDagPath ) and ( mi.shapeDagPath == exMi.shapeDagPath ):
						append = False
						break
						pass
					pass
				# Append if mesh info wasn't filtered out					
				if append:
					result.append( mi )
					pass
				pass
			pass
		return result
		pass

	## processSelection
	def processSelection( self, selList ):
		result = []
		# Process selection list
		it = OpenMaya.MItSelectionList( selList );
		while not it.isDone():
			#self.exportDagPath( xmlRoot, it.getDagPath(), path, fileName );
			if OpenMaya.MItSelectionList.kDagSelectionItem == it.itemType():
				dagPath = it.getDagPath()
				if dagPath.isVisible():
					tmpMeshInfos = self.findMayaMeshes( dagPath, result )
					result.extend( tmpMeshInfos )
				pass
			# Advance to next item
			it.next()
			pass
		# Return result
		return result			
		pass		

	## getMeshes
	def getMeshes( self ):
		selList = OpenMaya.MSelectionList()
		# Pull the path names using API 1.0 - build selection list
		it = OpenMaya_v1.MItDag( OpenMaya_v1.MItDag.kDepthFirst, OpenMaya_v1.MFn.kInvalid )
		while not it.isDone():
			dagPath = OpenMaya_v1.MDagPath()
			it.getPath( dagPath )
			if OpenMaya_v1.MFn.kTransform == dagPath.apiType():
				pathStr = dagPath.fullPathName()
				selList.add( pathStr )
				pass	
			it.next()
			pass
		# Find meshes
		result = self.processSelection( selList )
		# Return result
		return result
		pass

	## getMeshesSelected
	def getMeshesSelected( self ):
		selList = OpenMaya.MGlobal.getActiveSelectionList()
		# Find meshes
		result = self.processSelection( selList )
		# Return result
		return result		
		pass		

	# class BaseExporter
	pass

## export
def export( path, *args, **kwargs ):
	b = MayaExporter()
	b.export( path, args, kwargs )
	pass