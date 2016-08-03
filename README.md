# Cinder-3DTools

## Maya ##
TriMeshExporter is a simple and straightfoward exporter for polygon meshes from Maya to Cinder's TriMesh format. By default it exports geometry positions and normals in object (aka local) space with the tranform matrix written into the scene XML file. Options to control this behavior are in the next section.

Currently, all paths are relative to the scene XML. An option will be added later to force absolute paths if desired. Basic properties of ```lambert```, ```blinn```, ```phong```, ```phongE```, and ```anisotropic``` are exported as well. See the sample XML below.


The following options can be used to control the behavior of the exporter:
* ```bakeTransfrom``` - Default is False. If set to True, the export will use the world space coordinates for geometry positions and normals.
* ```angleWeightedNormals``` - Defaulti s False. If set to True, the normals will be angle weighted instead of averaged.


Example usage:
```python
import sys
sys.path.append( "C:/Users/hai/code/cinder/Cinder-3DTools/Maya/TriMeshExporter" )
import TriMeshExporter
reload( TriMeshExporter )
 
TriMeshExporter.exportSelected( "C:/Users/hai/code/cinder/Cinder-3DTools/TriMeshViewer/assets" )
```

To individually export geometry with world space coordinates, add a ``bool`` attribute called ``ciBakeTransform`` to a shape's direct transform parent.

If there is a ```file``` connection attached to a shader's ```color``` attribute. The geometry's color will be exported as ```[1, 1, 1]``` in the data. The file path will be be included in the export:
```xml
<param name="color" type="file" value="../textures/rg_grad.png"/>
```


## Cinder ##
Example usage:
```c++
std::vector<simplescene::Node> nodes = simplescene::load( getAssetPath( "Basic/Basic.xml" ) );
...
for( auto& node : nodes ) {
	node.draw();
}
```

## Simple Scene XML ##
```xml
<?xml version="1.0" ?>
<simplescene>
   <mesh name="pPlaneShape1" transform="1.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 1.0">
      <shaderSet name="lambert4" type="lambert">
         <shaderParams type="maya">
            <param name="color" type="file" value="../textures/rg_grad.png"/>
            <param name="transparency" type="color" valueB="0.0" valueG="0.0" valueR="0.0"/>
            <param name="ambientColor" type="color" valueB="0.0" valueG="0.0" valueR="0.0"/>
            <param name="incandescence" type="color" valueB="0.0" valueG="0.0" valueR="0.0"/>
            <param name="diffuse" type="float" value="0.800000011921"/>
            <param name="translucence" type="float" value="0.0"/>
         </shaderParams>
         <geometry triMeshFile="pPlane1.mesh" vertexCount="0"/>
      </shaderSet>
   </mesh>
   <mesh name="pTorusShape1" transform="1.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.634731961435 0.0 1.0">
      <shaderSet name="lambert3" type="lambert">
         <shaderParams type="maya">
            <param name="color" type="color" valueB="0.413100004196" valueG="0.386400014162" valueR="0.702199995518"/>
            <param name="transparency" type="color" valueB="0.0" valueG="0.0" valueR="0.0"/>
            <param name="ambientColor" type="color" valueB="0.0" valueG="0.0" valueR="0.0"/>
            <param name="incandescence" type="color" valueB="0.0" valueG="0.0" valueR="0.0"/>
            <param name="diffuse" type="float" value="0.800000011921"/>
            <param name="translucence" type="float" value="0.0"/>
         </shaderParams>
         <geometry triMeshFile="pTorus1.mesh" vertexCount="0"/>
      </shaderSet>
   </mesh>
</simplescene>
```
