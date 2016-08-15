
from TriMeshWriter import TriMeshWriter

## \class BaseMaterial
#
#
class BaseMaterial( object ):
	## c'tor
	def __init__( self ):
		print( "BaseMaterial c'tor" )		
		pass

	## getName
	def getName( self ):
		raise NotImplementedError()
		pass		

	## class BaseMaterial
	pass

## \class BaseMesh
#
#
class BaseMesh( object ):
	## c'tor
	def __init__( self ):
		print( "BaseMesh c'tor" )		
		pass

	## getName
	def getName( self ):
		raise NotImplementedError()
		pass

	## getTriMeshes
	def getTriMeshes( self ):
		raise NotImplementedError()
		pass		

	## class BaseMesh
	pass

## \class BaseCamera
#
#
class BaseCamera( object ):
	## c'tor
	def __init__( self ):
		print( "BaseCamera c'tor" )		
		pass

	## getName
	def getName( self ):
		raise NotImplementedError()
		pass

	## class BaseCamera
	pass

## \class BaseLight
#
#
class BaseLight( object ):
	## c'tor
	def __init__( self ):
		print( "BaseLight c'tor" )		
		pass

	## getName
	def getName( self ):
		raise NotImplementedError()
		pass

	## class BaseLight
	pass	

## \class BaseExporter
#
#
class BaseExporter( object ):
	## c'tor
	def __init__( self ):
		print( "BaseExporter c'tor" )
		self.path = None
		self.meshes = []
		pass

	## getMeshes
	def getMeshes( self ):
		raise NotImplementedError()
		pass

	## getMeshesSelected
	def getMeshesSelected( self ):
		raise NotImplementedError()
		pass

	## exportMeshes
	def exportMeshes( self ):
		# Bail if there's nothing to export
		if 0 == len( self.meshes ):
			print( "Nothing to export" )
			return
			pass
		# Export to requested file type
		tw = TriMeshWriter( self.path, self.meshes )
		tw.write()
		pass

	## export
	def export( self, path, *args, **kwargs ):
		self.path = path
		# Parse arguments
		selected = kwargs.get( "selected", False )
		# Get meshes
		if selected:
			self.meshes = self.getMeshesSelected()
		else:
			self.meshes = self.getMeshes()
			pass
		# Do export
		self.exportMeshes()
		pass

	# class BaseExporter
	pass