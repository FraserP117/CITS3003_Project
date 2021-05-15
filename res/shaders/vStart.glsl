#version 150

attribute vec3 vPosition;
attribute vec3 vNormal;
attribute vec2 vTexCoord;

varying vec2 texCoord;
varying vec4 color;

// added:
uniform float texScale;

uniform vec3 AmbientProduct, DiffuseProduct, SpecularProduct;
uniform mat4 ModelView;
uniform mat4 Projection;
uniform vec4 LightPosition;
uniform float Shininess;

void main()
{
    vec4 vpos = vec4(vPosition, 1.0);

    // Transform vertex position into eye coordinates
    vec3 pos = (ModelView * vpos).xyz;

    // The vector to the light from the vertex
    vec3 Lvec = LightPosition.xyz - pos; // using this one initially

    // ---------------------------------------------------------------
    // ADDED for part F
    // Parameters in the distance attenuation factor:
    float a;
    float b;
    float c;

    // Factors for PART F
    float distance;
    float distanceQuadratic;
    float attenuationFactor;

    // ADDED FOR PART F:
    a = 1.0;
    b = 0.5;
    c = 0.25;
    distance = length(Lvec);
    distanceQuadratic = a*(distance * distance) + b*distance + c;
    attenuationFactor = (1/distanceQuadratic);
    // ---------------------------------------------------------------

    // Unit direction vectors for Blinn-Phong shading calculation
    vec3 L = normalize( Lvec );   // Direction to the light source
    vec3 E = normalize( -pos );   // Direction to the eye/camera
    vec3 H = normalize( L + E );  // Halfway vector

    // Transform vertex normal into eye coordinates (assumes scaling
    // is uniform across dimensions)
    vec3 N = normalize( (ModelView*vec4(vNormal, 0.0)).xyz );

    // Compute terms in the illumination equation
    // PART F - multiply ambient, diffuse and specular by attenuationFactor??? (pretty sure)
    vec3 ambient = AmbientProduct;

    float Kd = max( dot(L, N), 0.0 );
    vec3  diffuse = Kd*DiffuseProduct;

    float Ks = pow( max(dot(N, H), 0.0), Shininess );
    vec3  specular = Ks * SpecularProduct;

    if (dot(L, N) < 0.0 ) {
	specular = vec3(0.0, 0.0, 0.0);
    }

    // globalAmbient is independent of distance from the light source
    vec3 globalAmbient = vec3(0.1, 0.1, 0.1);
    color.rgb = globalAmbient  + ((ambient + diffuse + specular) * attenuationFactor);
    color.a = 1.0;

    gl_Position = Projection * ModelView * vpos;
    // texCoord = vTexCoord;
    texCoord = vTexCoord * texScale;
}
