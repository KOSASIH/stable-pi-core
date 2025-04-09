// src/frontend/App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, TextField, Button, Typography, CircularProgress, Snackbar, Card, CardContent, Grid } from '@mui/material';
import MuiAlert from '@mui/material/Alert';
import { Bar } from 'react-chartjs-2';

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

function App() {
  const [strategy, setStrategy] = useState('');
  const [simulationId, setSimulationId] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');
  const [history, setHistory] = useState([]);

  useEffect(() => {
    // Load simulation history from local storage on component mount
    const savedHistory = JSON.parse(localStorage.getItem('simulationHistory')) || [];
    setHistory(savedHistory);
  }, []);

  const startSimulation = async () => {
    if (!strategy) {
      setError('Please enter a valid strategy.');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccessMessage('');
    try {
      const response = await axios.post('/api/simulate', { strategy });
      setSimulationId(response.data.simulationId);
      setSuccessMessage('Simulation started successfully!');
      // Update history
      const newHistory = [...history, { id: response.data.simulationId, strategy }];
      setHistory(newHistory);
      localStorage.setItem('simulationHistory', JSON.stringify(newHistory));
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to start simulation. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const fetchResults = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`/api/simulation/${simulationId}`);
      setResults(response.data.results);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to fetch results. Please check the simulation ID and try again.');
    } finally {
      setLoading(false);
    }
  };

  const clearInputs = () => {
    setStrategy('');
    setSimulationId('');
    setResults(null);
  };

  const renderResultsChart = () => {
    if (!results || results.length === 0) return null;

    const data = {
      labels: results.map((_, index) => `Result ${index + 1}`),
      datasets: [
        {
          label: 'Simulation Results',
          data: results,
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
        },
      ],
    };

    return <Bar data={data} />;
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" align="center" gutterBottom>
        Trans-Reality Quantum Forge Dashboard
      </Typography>
      <TextField
        fullWidth
        label="Enter your strategy"
        variant="outlined"
        value={strategy}
        onChange={(e) => setStrategy(e.target.value)}
        margin="normal"
      />
      <Button variant="contained" color="primary" onClick={startSimulation} disabled={loading}>
        Start Simulation
      </Button>
      <Button variant="outlined" color="secondary" onClick={fetchResults} disabled={!simulationId || loading}>
        Get Results
      </Button>
      <Button variant="text" onClick={clearInputs} disabled={loading}>
        Clear
      </Button>
      {loading && <CircularProgress />}
      {results && (
        <Card style={{ marginTop: '20px' }}>
          <CardContent>
            <Typography variant="h5">Results:</Typography>
            {renderResultsChart()}
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
      <Typography variant="h6" gutterBottom style={{ marginTop: '20px' }}>
        Simulation History
      </Typography>
      <Grid container spacing={2}>
        {history.map((item) => (
          <Grid item xs={12} key={item.id}>
            <Card>
              <CardContent>
                <Typography variant="body1">Simulation ID: {item.id}</Typography>
                <Typography variant="body2">Strategy: {item.strategy}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}

export default App;
