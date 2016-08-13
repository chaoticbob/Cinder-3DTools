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

#include "cinder/app/App.h"
#include "cinder/app/RendererGl.h"
#include "cinder/gl/gl.h"
#include "cinder/Camera.h"
#include "cinder/TriMesh.h"
using namespace ci;
using namespace ci::app;
using namespace std;

#include "simplescene/SimpleScene.h"
namespace ss = simplescene;

//! \class TriMeshViewerApp
//!
//!
class TriMeshViewerApp : public App {
public:
	void setup() override;
	void mouseDown( MouseEvent event ) override;
	void update() override;
	void draw() override;

private:
	CameraPersp				mCam;
	std::vector<ss::Node>	mNodes;

	gl::Texture2dRef		mTex;
};

void TriMeshViewerApp::setup()
{
	//mCam.lookAt( vec3( 2, 17, 20 ), vec3( 0, 0, 0 ) );
	mCam.lookAt( vec3( -5, 4, -15 ), vec3( 0, 0, 0 ) );
	mNodes = ss::load( getAssetPath( "Untitled_3/Untitled_3.xml" ) );

	//mTex = gl::Texture2d::create( loadImage( getAssetPath( "textures/photo_1.jpg" ) ) );
}

void TriMeshViewerApp::mouseDown( MouseEvent event )
{
}

void TriMeshViewerApp::update()
{
}

void TriMeshViewerApp::draw()
{
	gl::clear( Color( 0.3f, 0.65f, 0.65f ) ); 
	gl::enableDepth();

	gl::setMatrices( mCam );
	//gl::multViewMatrix( glm::scale( vec3( -1, 1, 1 ) ) * glm::rotate( 3.141592f, vec3( 0, 1, 0 ) ) );
	//gl::multViewMatrix( glm::scale( vec3( -1, 1, 1 ) ) );

	//gl::rotate( 0.5f * getElapsedSeconds(), 0, 1, 0 );
	//gl::rotate( 0.2f * getElapsedSeconds(), 1, 0, 0 );
	//gl::scale( vec3( 1.0f + 0.10f * sin( 2.0f * getElapsedSeconds() ) ) );

	for( auto& node : mNodes ) {
		//gl::ScopedTextureBind texBind( mTex, 0 );
		node.getBatch()->getGlslProg()->uniform( "uTex0", 0 );
		node.draw();
	}
}

void prepareSettings( App::Settings *settings ) 
{
	settings->setWindowSize( 960, 720 );
}

CINDER_APP( TriMeshViewerApp, RendererGl, prepareSettings )
