
class BaseExporter( object ):
	def __init__( self ):
		print( "BaseExporter c'tor" )
		pass

	def export( self, path, *args, **kwargs ):
		raise NotImplementedError()
		pass

	# class BaseExporter
	pass