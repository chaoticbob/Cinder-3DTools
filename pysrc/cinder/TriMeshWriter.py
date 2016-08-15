
## \class TriMeshWriter
#
#
class TriMeshWriter( object ):
	## c'tor
	def __init__( self, path, meshes ):
		self.path = path
		self.meshes = meshes
		pass

	## writeMeshes
	def write( self ):
		for mesh in self.meshes:
			print mesh.getName()
		pass

	# class TriMeshWriter
	pass