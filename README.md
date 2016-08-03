# Cinder-3DTools

## Maya ##
Example usage:
```
import sys
sys.path.append( "C:/Users/hai/code/cinder/Cinder-3DTools/Maya/TriMeshExporter" )
import TriMeshExporter
reload( TriMeshExporter )
 
TriMeshExporter.exportSelected( "C:/Users/hai/code/cinder/Cinder-3DTools/TriMeshViewer/assets" )
```

## Cinder ##
Example usage:
```
std::vector<simplescene::Node> nodes = simplescene::load( getAssetPath( "Basic/Basic.xml" ) );
```
