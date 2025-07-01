function helloTriangle() {
  /** @type {HTMLCanvasElement | null} */
  const surface = document.getElementById("surface");
  if (!surface) {
    console.error('Canvas element with id "surface" not found.');
    return;
  }

  /** @type {WebGL2RenderingContext | null} */
  const gl = surface.getContext('webgl2');
  if (!gl) {
    console.error('WebGL2 context could not be initialized.');
    return;
  }

  gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);

  const vertexData = new Float32Array([
    //  x    y    r    g    b
     0.0,  0.5,  0.0, 1.0, 0.0,  // top vertex - green
    -0.5, -0.5, 1.0, 0.0, 0.0,  // bottom-left - red
     0.5, -0.5, 0.0, 0.0, 1.0   // bottom-right - blue
  ]);

  const vertexBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, vertexData, gl.DYNAMIC_DRAW);

  const vxShCode = `#version 300 es
  precision mediump float;
  in vec2 vertexPosition;
  in vec3 vertexColor;
  out vec3 fragColor;
  uniform mat4 rotation;

  void main() {
    vec4 pos = vec4(vertexPosition, 0.0, 1.0);
    gl_Position = rotation * pos;
    fragColor = vertexColor;
  }`;

  const fragmentShaderSourceCode = `#version 300 es
  precision mediump float;
  in vec3 fragColor;
  out vec4 outputColor;

  void main() {
    outputColor = vec4(fragColor, 1.0);
  }`;

  function compileShader(type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      console.error((type === gl.VERTEX_SHADER ? "Vertex" : "Fragment") + " Shader Error:", gl.getShaderInfoLog(shader));
      return null;
    }
    return shader;
  }

  const vertexShader = compileShader(gl.VERTEX_SHADER, vxShCode);
  const fragmentShader = compileShader(gl.FRAGMENT_SHADER, fragmentShaderSourceCode);
  if (!vertexShader || !fragmentShader) return;

  const program = gl.createProgram();
  gl.attachShader(program, vertexShader);
  gl.attachShader(program, fragmentShader);
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    console.error("Program Link Error:", gl.getProgramInfoLog(program));
    return;
  }

  gl.useProgram(program);

  const stride = 5 * Float32Array.BYTES_PER_ELEMENT;

  const posLocation = gl.getAttribLocation(program, "vertexPosition");
  gl.enableVertexAttribArray(posLocation);
  gl.vertexAttribPointer(posLocation, 2, gl.FLOAT, false, stride, 0);

  const colorLocation = gl.getAttribLocation(program, "vertexColor");
  gl.enableVertexAttribArray(colorLocation);
  gl.vertexAttribPointer(colorLocation, 3, gl.FLOAT, false, stride, 2 * Float32Array.BYTES_PER_ELEMENT);

  const rotationLoc = gl.getUniformLocation(program, "rotation");

  function animate(time) {
    gl.clearColor(32 / 255, 37 / 255, 44 / 255, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    const angle = time * 0.002;
    const axis = [time + Math.E*69, (time+69) / Math.PI, time];

    // Normalize axis
    const len = Math.hypot(...axis);
    const [x, y, z] = axis.map(v => v / len);
    const c = Math.cos(angle);
    const s = Math.sin(angle);
    const t = 1 - c;

    const rotMatrix = new Float32Array([
      t*x*x + c,     t*x*y - s*z, t*x*z + s*y, 0,
      t*x*y + s*z,   t*y*y + c,   t*y*z - s*x, 0,
      t*x*z - s*y,   t*y*z + s*x, t*z*z + c,   0,
      0,             0,           0,           1
    ]);
    gl.uniformMatrix4fv(rotationLoc, false, rotMatrix);

    // Color cycle logic
    const r = Math.abs(Math.sin(time * 0.001));
    const g = Math.abs(Math.sin(time * 0.001 + 2));
    const b = Math.abs(Math.sin(time * 0.001 + 4));

    vertexData.set([
      Math.sin(time/100), 0.5, 0, 1, 0,
     Math.cos(time/100 + 6.9), -0.5, 1, 0, 0,
      0.5, Math.cos(time/100), 0, 0, 1
    ]);
    gl.bufferSubData(gl.ARRAY_BUFFER, 0, vertexData);

    gl.drawArrays(gl.TRIANGLES, 0, 3);
    requestAnimationFrame(animate);
  }

  requestAnimationFrame(animate);
}

try {
  helloTriangle();
} catch (e) {
  console.error("Error during helloTriangle execution:", e);
}