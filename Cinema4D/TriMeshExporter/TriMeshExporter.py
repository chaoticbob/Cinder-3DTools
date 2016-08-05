
import c4d

class _c4d( object ):
	OBJECT_POLYGON = 5100
	pass

class TriMeshExporter( object ):
	def __init__( self ):
		pass

	## createFilePath
	def exportSelected( self, path, bakeTranform, angleWeightedNormals ):
		doc = c4d.documents.GetActiveDocument()
	
		selected = doc.GetActiveObjects( c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER )
		for obj in selected:
			if _c4d.OBJECT_POLYGON != obj.GetType():
				print( "%s : %d" % ( obj.GetName(), obj.GetType() ) )
				pass

		pass

	# class TriMeshExporter 		
	pass

def exportSelected( path, *args, **kwargs ):
	# Error check arguments
	validKeys = ["bakeTransform", "angleWeightedNormals"]
	for key in kwargs.keys():
		if key not in validKeys:
			raise RuntimeError( "Unknown paramemter: %s" % key )
	# Grab arguemnts
	bakeTransform = kwargs.get( "bakeTransform", False )
	angleWeightedNormals = kwargs.get( "angleWeightedNormals", False )
	# Run exporter
	# Run exporter
	exporter = TriMeshExporter()
	exporter.exportSelected( path, bakeTransform, angleWeightedNormals )
	pass