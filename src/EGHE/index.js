// src/EGHE/index.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Typography, Button, Snackbar, CircularProgress, Card, CardContent, Grid, TextField } from '@mui/material';
import MuiAlert from '@mui/material/Alert';
import { Bar } from 'react-chartjs-2';

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

function EGHE() {
  const [gravityData, setGravityData] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');
  const [history, setHistory] = useState([]);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const fetchGravityData = async () => {
      setLoading(true);
      try {
        const response = await axios.get('/api/gravity-data');
        setGravityData(response.data);
        setSuccessMessage('Gravity data fetched successfully!');
      } catch (err) {
        setError('Failed to fetch gravity data.');
      } finally {
        setLoading(false);
      }
    };

    if (isAuthenticated) {
      fetchGravityData();
    }
  }, [isAuthenticated]);

  const handleLogin = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('/api/login', { username, password });
      if (response.data.success) {
        setIsAuthenticated(true);
        setSuccessMessage('Login successful!');
      } else {
        setError('Invalid credentials.');
      }
    } catch (err) {
      setError('Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const predictGravityChanges = async () => {
    if (!gravityData) {
      setError('No gravity data available for prediction.');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('/api/predict-gravity', { data: gravityData });
      setPredictions(response.data.predictions);
      setSuccessMessage('Predictions generated successfully!');
      // Update history
      const newHistory = [...history, { gravityData, predictions: response.data.predictions }];
      setHistory(newHistory);
      localStorage.setItem('predictionHistory', JSON.stringify(newHistory));
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to generate predictions.');
    } finally {
      setLoading(false);
    }
  };

  const activateProtectionProtocols = () => {
    if (predictions && predictions.some(prediction => prediction.alert)) {
      console.log('Activating protection protocols...');
      setSuccessMessage('Protection protocols activated!');
    } else {
      setError('No extreme conditions detected.');
    }
  };

  const renderPredictionsChart = () => {
    if (!predictions || predictions.length === 0) return null;

    const data = {
      labels: predictions.map((_, index) => `Prediction ${index + 1}`),
      datasets: [
        {
          label: 'Predicted Gravity Changes',
          data: predictions.map(prediction => prediction.value), // Assuming predictions have a 'value' property
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
        },
      ],
    };

    return <Bar data={data} />;
  };

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" align="center" gutterBottom>
        Eternal Gravitational Harmony Engine
      </Typography>
      {!isAuthenticated ? (
        <Card style={{ marginBottom: '20px' }}>
          <CardContent>
            <Typography variant="h5">Login</Typography>
            <TextField
              label="Username"
              variant="outlined"
              fullWidth
              margin="normal"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <TextField
              label="Password"
              type="password"
              variant="outlined"
              fullWidth
              margin="normal"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button variant="contained" color="primary" onClick={handleLogin} disabled={loading}>
              Login
            </Button>
          </CardContent>
        </Card>
      ) : (
        <>
          <Button variant="contained" color="primary" onClick={predictGravityChanges} disabled={loading}>
            Predict Gravity Changes
          </Button>
          <Button variant="outlined" color="secondary" onClick={activateProtectionProtocols} disabled={!predictions}>
            Activate Protection Protocols
          </Button>
          {loading && <CircularProgress />}
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
          {predictions && (
            <Card style={{ marginTop: '20px' }}>
              <CardContent>
                <Typography variant="h6">Predictions:</Typography>
                {renderPredictionsChart()}
                <pre>{JSON.stringify(predictions, null, 2)}</pre>
              </CardContent>
            </Card>
          )}
          <Typography variant="h6" gutterBottom style={{ marginTop: '20px' }}>
            Prediction History
          </Typography>
          <Grid container spacing={2}>
            {history.map((item, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Card>
                  <CardContent>
                    <Typography variant="body1">Gravity Data: {JSON.stringify(item.gravityData)}</Typography>
                    <Typography variant="body2">Predictions: {JSON.stringify(item.predictions)}</Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </>
      )}
    </Container>
  );
}

export default EGHE;
