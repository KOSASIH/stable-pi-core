// src/ODNC/index.js
import React, { useState } from 'react';
import axios from 'axios';
import { Container, Typography, Button, TextField, Snackbar, Alert, Card, CardContent, Grid, CircularProgress } from '@mui/material';

function ODNC() {
  const [energyType, setEnergyType] = useState('');
  const [amount, setAmount] = useState('');
  const [predictionData, setPredictionData] = useState([]);
  const [conversionHistory, setConversionHistory] = useState([]);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleEnergyConversion = async () => {
    if (!energyType || !amount) {
      setError('Please enter both energy type and amount.');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('/api/convert-energy', { energyType, amount: parseFloat(amount) });
      const convertedAmount = response.data.result;
      setSuccessMessage(`Converted Amount: ${convertedAmount}`);
      // Update conversion history
      setConversionHistory([...conversionHistory, { energyType, amount: parseFloat(amount), convertedAmount }]);
    } catch (err) {
      setError(err.response?.data?.message || 'Energy conversion failed.');
    } finally {
      setLoading(false);
    }
  };

  const handleResourcePrediction = async () => {
    if (!energyType || !amount) {
      setError('Please enter both energy type and amount.');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('/api/predict-extraction', { energyData: [{ type: energyType, amount: parseFloat(amount) }] });
      setPredictionData(response.data.prediction);
      setSuccessMessage('Prediction generated successfully!');
    } catch (err) {
      setError(err.response?.data?.message || 'Resource prediction failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" align="center" gutterBottom>
        Omni-Dimensional Nexus Converter
      </Typography>
      <TextField
        label="Energy Type"
        variant="outlined"
        fullWidth
        margin="normal"
        value={energyType}
        onChange={(e) => setEnergyType(e.target.value)}
      />
      <TextField
        label="Amount"
        type="number"
        variant="outlined"
        fullWidth
        margin="normal"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />
      <Button variant="contained" color="primary" onClick={handleEnergyConversion} disabled={loading}>
        Convert Energy
      </Button>
      <Button variant="outlined" color="secondary" onClick={handleResourcePrediction} style={{ marginTop: '10px' }} disabled={loading}>
        Predict Resource Extraction
      </Button>
      {loading && <CircularProgress style={{ marginTop: '20px' }} />}
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
      {predictionData.length > 0 && (
        <Card style={{ marginTop: '20px' }}>
          <CardContent>
            <Typography variant="h6">Predicted Resource Extraction:</Typography>
            <ul>
              {predictionData.map((item, index) => (
                <li key={index}>
                  {item.type}: {item.predictedValue.toFixed(2)}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
      {conversionHistory.length > 0 && (
        <div style={{ marginTop: '20px' }}>
          <Typography variant="h6">Conversion History:</Typography>
          <Grid container spacing={2}>
            {conversionHistory.map((entry, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Card>
                  <CardContent>
                    <Typography variant="body1">Energy Type: {entry.energyType}</Typography>
                    <Typography variant="body2">Amount: {entry.amount}</Typography>
                    <Typography variant="body2">Converted Amount: {entry.convertedAmount}</Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </div>
      )}
    </Container>
  );
}

export default ODNC;
