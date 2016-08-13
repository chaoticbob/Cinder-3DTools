/*
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
*/

#include "SimpleScene.h"

#include "cinder/Log.h"
#include "cinder/Utilities.h"
#include "cinder/Xml.h"
using namespace ci;

namespace simplescene {

Node::Node()
{

}

Node::Node( const ci::mat4 &transform, const ci::gl::BatchRef &batch, const ci::gl::Texture2dRef &colorTexture )
	: mTransform( transform ), mBatch( batch ), mColorTexture( colorTexture )
{

}

Node::~Node()
{

}

void Node::draw()
{
	if( ! mBatch ) {
		return;
	}

	gl::ScopedViewMatrix scopedViewMatrix;
	gl::multViewMatrix( glm::scale( vec3( -1, 1, 1 ) ) );

	gl::ScopedModelMatrix scopedModel;
	if( mTransformEnabled ) {
		gl::rotate( 3.141592, vec3( 0, 1, 0 ) );
		gl::multModelMatrix( mTransform );
	}

	if( mColorTexture ) {
		gl::ScopedTextureBind scopedTexture( mColorTexture );
		mBatch->draw();
	}
	else {
		mBatch->draw();
	}
}

std::vector<Node> load( const ci::fs::path &sceneXml )
{
	std::vector<Node> result;

	fs::path dirName = sceneXml.parent_path();
	
	if( fs::exists( sceneXml ) ) {
		XmlTree xml = XmlTree( loadFile( sceneXml ) );
		for( auto meshElem = xml.begin( "simplescene/mesh" ); meshElem != xml.end(); ++meshElem ) {
			auto meshXml = *meshElem;

			ci::mat4 transform = ci::mat4();
			std::string transformStr = meshXml["transform"];
			auto transformElemsStr = ci::split( transformStr, " " );
			if( 16 == transformElemsStr.size() ) {
				float *m = &(transform[0][0]);
				for( size_t i = 0; i < 16; ++i ) {
					m[i] = std::stof( transformElemsStr[i] );
				}
			}

			for( auto shaderSetElem = meshXml.begin( "shaderSet" ); shaderSetElem != meshXml.end(); ++shaderSetElem ) {
				auto shaderSetXml = *shaderSetElem;
				auto geoXml = shaderSetXml / "geometry";

				// Skip if there's no geometry
				if( ! geoXml.hasAttribute( "triMeshFile" ) ) {
					continue;
				}

				// Find color texture
				gl::Texture2dRef colorTexture;
				if( shaderSetXml.hasChild( "shaderParams" ) ) {
					auto shaderParamsXml = shaderSetXml / "shaderParams";
					for( auto paramElem = shaderParamsXml.begin( "param" ); paramElem != shaderParamsXml.end(); ++paramElem ) {
						auto paramXml = *paramElem;
						std::string name = paramXml["name"];
						std::string type = paramXml["type"];
						std::string value = paramXml["value"];
						if( ( "color" == name ) && ( "file" == type ) && ( ! value.empty() ) ) {
							fs::path imagePath = dirName / value;
							try {
								colorTexture = gl::Texture2d::create( loadImage( imagePath ) );
								CI_LOG_I( "Created texture using " << imagePath );
							}
							catch( const std::exception &e ) {
								CI_LOG_E( "Failed to load texture at " << imagePath << " (" << e.what() << ")" );
							}
						}
					}
				}
								
				TriMesh triMesh;
				bool triMeshLoaded = false;
				fs::path triMeshPath = dirName / std::string( geoXml["triMeshFile"] );

				try {
					triMesh.read( loadFile( triMeshPath ) );
					triMeshLoaded = true;
					CI_LOG_I( "Loaded trimesh from " << triMeshPath );
				}
				catch( const std::exception &e ) {
					CI_LOG_E( "Failed to load trimesh at " << triMeshPath << " (" << e.what() << ")" );
				}
		
				if( triMeshLoaded ) {
					gl::GlslProgRef glslProg;
					if( colorTexture ) {
						glslProg = gl::context()->getStockShader( gl::ShaderDef().color().texture().lambert() );
					}
					else {
						glslProg = gl::context()->getStockShader( gl::ShaderDef().color().lambert() );
					}

					gl::BatchRef batch = gl::Batch::create( triMesh, glslProg );
					simplescene::Node node = simplescene::Node( transform, batch, colorTexture );
					result.push_back( node );
				}
			}
		}
	}

	return result;
}

} // namespace simplescene