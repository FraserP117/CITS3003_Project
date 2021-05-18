
varying vec2 texCoord;  // The third coordinate is always 0.0 and is discarded

uniform sampler2D texture;
uniform float texScale;

// added - for the computation of the lighting equation in part G:
uniform vec3 AmbientProduct, DiffuseProduct, SpecularProduct;
uniform mat4 ModelView;
uniform mat4 Projection;
uniform float Shininess;

// Light Object 1
uniform vec4 LightPosition;
uniform vec3 LightColor;
uniform float Brightness;
uniform vec4 LightObj; //

// PART I. Light Object 2
uniform vec4 LightPosition_2;
uniform vec3 LightColor_2;
uniform float Brightness_2;
uniform vec4 LightObj_2; //

varying vec3 white;

// the world-space origin:
uniform vec4 worldOrigin;


varying vec3 v_Position; // this v_Position value is from the vertex shader
varying vec3 v_Normal;   // the normal is also from the vertex shader

vec4 color;

void main()
{
    // vec4 vpos = vec4(vPosition, 1.0); // OG
    vec4 vpos = vec4(v_Position, 1.0);

    // Transform vertex position into eye coordinates
    vec3 pos = (ModelView * vpos).xyz;

    // The vector to the first light from the vertex
    vec3 Lvec = LightPosition.xyz - pos; // using this one initially

    // The vector to the second light from the vertex
    // vec3 Lvec_2 = LightPosition_2.xyz; // this isn't right
    vec3 Lvec_2 = LightPosition_2.xyz - worldOrigin.xyz;

    // Unit direction vectors for Blinn-Phong shading calculation (first light)
    vec3 L = normalize( Lvec );   // Direction to the light source
    vec3 C = normalize( -pos );   // Direction to the camera
    vec3 H = normalize( L + C );  // Halfway vector

    // Unit direction vectors for Blinn-Phong shading calculation (second light)
    vec3 L_2 = normalize( Lvec_2 );   // Direction to the light source
    vec3 C_2 = normalize( -pos );   // Direction to the camera
    vec3 H_2 = normalize( L_2 + C );  // Halfway vector

    // ---------------------------------------------------------------

    // Factors for PART G
    float distance;
    float distanceQuadratic;
    float attenuationFactor;

    // ADDED for part G
    // Parameters in the distance attenuation factor:
    float a;
    float b;
    float c;

    // ADDED FOR PART G:
    a = 1.0;
    b = 0.5;
    c = 0.25;
    distance = length(Lvec);
    distanceQuadratic = a*(distance * distance) + b*distance + c;
    attenuationFactor = (1.0/distanceQuadratic);
    // ---------------------------------------------------------------

    // Transform vertex normal into eye coordinates (assumes scaling
    // is uniform across dimensions).
    vec3 N = normalize( (ModelView*vec4(v_Normal, 0.0)).xyz );

    // Compute terms in the illumination equation:
    // First; we calculate the ambient term:
    vec3 ambient = LightColor * AmbientProduct;
    vec3 ambient_2 = LightColor_2 * AmbientProduct;

    // second; the diffuse term:
    float Kd = max( dot(L, N), 0.0 );
    vec3  diffuse = LightColor * Kd * DiffuseProduct;
    float Kd_2 = max( dot(L, N), 0.0 );
    vec3  diffuse_2 = LightColor_2 * Kd_2 * DiffuseProduct;

    // third; the specuar term:

    vec3 white = vec3(1.0, 1.0, 1.0);

    float Ks = pow( max(dot(N, H), 0.0), Shininess );
    vec3  specular = Brightness * Ks * SpecularProduct * white;
    float Ks_2 = pow( max(dot(N, H_2), 0.0), Shininess );
    vec3  specular_2 = Brightness_2 * Ks_2 * SpecularProduct * white;

    // can't have negative dot product for specualr term:
    if (dot(L, N) < 0.0 ) {
        specular = vec3(0.0, 0.0, 0.0);
    }
    if (dot(L_2, N) < 0.0 ) {
        specular = vec3(0.0, 0.0, 0.0);
    }

    // globalAmbient is independent of distance from the light source
    vec3 globalAmbient = vec3(0.1, 0.1, 0.1);

    // color.rgb = globalAmbient  + ((ambient + diffuse + specular) * attenuationFactor);
    // color.rgb = (globalAmbient  + (((ambient + ambient_2) + (diffuse + diffuse_2) + (specular + specular_2)) * attenuationFactor));

    // color.rgb = (globalAmbient  + (((ambient + ambient_2) + (diffuse + diffuse_2)) * attenuationFactor));
    color.rgb = globalAmbient  + (((ambient + ambient_2) + (diffuse + diffuse_2)) * attenuationFactor);
    color.a = 1.0;

    // gl_FragColor = color * texture2D( texture, texCoord * 2.0 );
    // specular is vec3 and (color * texture) = vec4

    vec4 attenuated_specular_terms = vec4(((specular + specular_2) * attenuationFactor), 1.0);
    gl_FragColor = (color * texture2D( texture, texCoord * 2.0 )) + attenuated_specular_terms;

    // gl_FragColor = (color * texture2D( texture, texCoord * 2.0 )) + ((specular + specular_2) * attenuationFactor);
}
