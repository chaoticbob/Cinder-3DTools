
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
		for itObj in selected:
			obj = itObj
			if _c4d.OBJECT_POLYGON != obj.GetType():
				tmpObj = obj.GetClone()
				tmpList = c4d.utils.SendModelingCommand( command = c4d.MCOMMAND_CURRENTSTATETOOBJECT, list = [tmpObj], mode = c4d.MODELINGCOMMANDMODE_ALL, doc = doc )
				if len( tmpList ) > 0:
					obj = tmpList[0]
				pass
			
			print obj.GetAllPoints()
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