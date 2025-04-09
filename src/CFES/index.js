// src/CFES/index.js
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Container, Typography, Button, Snackbar, Alert, TextField, Card, CardContent, CircularProgress } from '@mui/material';
import { Canvas } from 'react-three-fiber'; // Using react-three-fiber for WebGL rendering

function CFES() {
  const [fractal, setFractal] = useState(null);
  const [userFeedback, setUser Feedback] = useState('');
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [fractalType, setFractalType] = useState('Mandelbrot');
  const [width, setWidth] = useState(800);
  const [height, setHeight] = useState(800);
  const [maxIterations, setMaxIterations] = useState(100);
  const [cX, setCX] = useState(-0.7);
  const [cY, setCY] = useState(0.27015);
  const [colorScheme, setColorScheme] = useState('grayscale'); // New state for color scheme

  useEffect(() => {
    if (fractal) {
      drawFractal();
    }
  }, [fractal]);

  const drawFractal = () => {
    // This function will be replaced with WebGL rendering logic
  };

  const handleGenerateFractal = async () => {
    setLoading(true);
    setError(null);
    setSuccessMessage(null);

    // Input validation
    if (width <= 0 || height <= 0 || maxIterations <= 0) {
      setError('Width, height, and max iterations must be positive numbers.');
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post('/api/generate-fractal', {
        type: fractalType,
        width: parseInt(width),
        height: parseInt(height),
        maxIterations: parseInt(maxIterations),
        cX: parseFloat(cX),
        cY: parseFloat(cY),
      });
      setFractal(response.data.fractal);
      setSuccessMessage('Fractal generated successfully!');
    } catch (err) {
      setError('Fractal generation failed.');
    } finally {
      setLoading(false);
    }
  };

  const handleEvolveFractal = async () => {
    if (!fractal) {
      setError('No fractal to evolve.');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccessMessage(null);

    try {
      const response = await axios.post('/api/evolve-fractal', { fractalId: fractal.id, userFeedback });
      setFractal(response.data.evolvedFractal);
      setSuccessMessage('Fractal evolved successfully!');
    } catch (err) {
      setError('Fractal evolution failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" align="center" gutterBottom>
        Cosmo-Fractal Evolution Synthesizer
      </Typography>
      <TextField
        label="Fractal Type"
        variant="outlined"
        fullWidth
        margin="normal"
        value={fractalType}
        onChange={(e) => setFractalType(e.target.value)}
      />
      <TextField
        label="Width"
        type="number"
        variant="outlined"
        fullWidth
        margin="normal"
        value={width}
        onChange={(e) => setWidth(e.target.value)}
      />
      <TextField
        label="Height"
        type="number"
        variant="outlined"
        fullWidth
        margin="normal"
        value={height}
        onChange={(e) => setHeight(e.target.value)}
      />
      <TextField
        label="Max Iterations"
        type="number"
        variant="outlined"
        fullWidth
        margin="normal"
        value={maxIterations}
        onChange={(e) => setMaxIterations(e.target.value)}
      />
      <TextField
        label="cX (for Julia set)"
        type="number"
        variant="outlined"
        fullWidth
        margin="normal"
        value={cX}
        onChange={(e) => setCX(e.target.value)}
      />
      <TextField
        label="cY (for Julia set)"
        type="number"
        variant="outlined"
        fullWidth
        margin="normal"
        value={cY}
        onChange={(e) => setCY(e.target.value)}
      />
      <TextField
        label="Color Scheme"
        variant="outlined"
        fullWidth
        margin="normal"
        value={colorScheme}
        onChange={(e) => setColorScheme(e.target.value)}
      />
      <Button variant="contained" color="primary" onClick={handleGenerateFractal} disabled={loading}>
        Generate Fractal
      </Button>
      {loading && <CircularProgress style={{ marginTop: '20px' }} />}
      {fractal && (
        <Card style={{ marginTop: '20px' }}>
          <CardContent>
            <Typography variant="h6">Fractal ID: {fractal.id}</Typography>
            <Canvas style={{ width: '100%', height: 'auto' }}>
              {/* WebGL rendering logic will go here */}
            </Canvas>
            <TextField
              label="User  Feedback"
              variant="outlined"
              fullWidth
              margin="normal"
              value={userFeedback}
              onChange={(e) => setUser Feedback(e.target.value)}
            />
            <Button variant="outlined" color="secondary" onClick={handleEvolveFractal} style={{ marginTop: '10px' }} disabled={loading}>
              Evolve Fractal
            </Button>
          </CardContent>
        </Card>
      )}
      <Snackbar open={!!error} autoHideDuration={6000} onClose={() => setError(null)}>
        <Alert onClose={() => setError(null)} severity="error">
          {error}
        </Alert>
      </Snackbar>
      <Snackbar open={!!successMessage} autoHideDuration={6000} onClose={() => setSuccessMessage('')}>
        <Alert onClose={() => setSuccessMessage('')} severity="success">
          {successMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
}

export default CFES;
