#version 150

attribute vec3 vPosition;
attribute vec2 vTexCoord;
attribute vec3 vNormal; // added; need this in the fragment shader I think

varying vec2 texCoord;

// added:
uniform float texScale;
uniform mat4 ModelView;
uniform mat4 Projection;

varying vec3 v_Position; // we must pass these to the fragment shader
varying vec3 v_Normal; // we must pass these to the fragment shader

// the only thing that should remain in the vertex shader is the transformation
// of the vertices and the normal into camera space. We then pass the position
// and the normal to the fragment shader in order to be able to perfrom the
// lighting calulations there; for smoother lighting results.

void main()
{
    v_Position = vPosition;
    v_Normal = vNormal;
    vec4 vpos = vec4(vPosition, 1.0); // need this

    texCoord = vTexCoord * texScale;

    // Transform vertex position into eye coordinates
    // vec3 pos = (ModelView * vpos).xyz;


    gl_Position = Projection * ModelView * vpos; // need this
}
