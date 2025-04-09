// src/CFES/fractalAlgorithm.js

const generateUniqueId = () => {
  return 'fractal-' + Math.random().toString(36).substr(2, 9);
};

// Function to generate a Mandelbrot set fractal
const generateMandelbrot = (width, height, maxIterations) => {
  const fractal = {
    id: generateUniqueId(),
    type: 'Mandelbrot',
    pattern: [],
  };

  for (let x = 0; x < width; x++) {
    for (let y = 0; y < height; y++) {
      let zx = 0;
      let zy = 0;
      let iteration = 0;
      const cX = (x / width) * 4 - 2; // Scale to [-2, 2]
      const cY = (y / height) * 4 - 2; // Scale to [-2, 2]

      while (zx * zx + zy * zy < 4 && iteration < maxIterations) {
        const tmp = zx * zx - zy * zy + cX;
        zy = 2 * zx * zy + cY;
        zx = tmp;
        iteration++;
      }

      // Color based on the number of iterations
      const color = iteration === maxIterations ? 0 : (iteration / maxIterations) * 255;
      fractal.pattern.push(color);
    }
  }

  return fractal;
};

// Function to generate a Julia set fractal
const generateJulia = (width, height, maxIterations, cX, cY) => {
  const fractal = {
    id: generateUniqueId(),
    type: 'Julia',
    pattern: [],
  };

  for (let x = 0; x < width; x++) {
    for (let y = 0; y < height; y++) {
      let zx = (x / width) * 4 - 2; // Scale to [-2, 2]
      let zy = (y / height) * 4 - 2; // Scale to [-2, 2]
      let iteration = 0;

      while (zx * zx + zy * zy < 4 && iteration < maxIterations) {
        const tmp = zx * zx - zy * zy + cX;
        zy = 2 * zx * zy + cY;
        zx = tmp;
        iteration++;
      }

      // Color based on the number of iterations
      const color = iteration === maxIterations ? 0 : (iteration / maxIterations) * 255;
      fractal.pattern.push(color);
    }
  }

  return fractal;
};

// Function to generate a fractal based on user choice
const generateFractal = (type, width = 800, height = 800, maxIterations = 100, cX = -0.7, cY = 0.27015) => {
  if (type === 'Mandelbrot') {
    return generateMandelbrot(width, height, maxIterations);
  } else if (type === 'Julia') {
    return generateJulia(width, height, maxIterations, cX, cY);
  } else {
    throw new Error('Unknown fractal type');
  }
};

// Evolve fractal based on user feedback
const evolveFractal = (fractalId, userFeedback) => {
  // Logic to evolve the fractal based on user feedback
  // This is a placeholder for actual evolution logic
  const evolvedFractal = {
    id: fractalId,
    pattern: [], // New evolved pattern
  };

  // Modify the fractal pattern based on feedback (this is a simplified example)
  for (let i = 0; i < 100; i++) {
    evolvedFractal.pattern.push(Math.random() + parseFloat(userFeedback)); // Simulated evolution
  }

  return evolvedFractal;
};

module.exports = { generateFractal, evolveFractal };
