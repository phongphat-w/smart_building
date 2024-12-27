import express from 'express';
import fetch from 'node-fetch';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();

const app = express();
const port = process.env.REACT_APP_SB_PORT;

// Access API URL from .env file
const API_URL = process.env.REACT_APP_SB_API_URL;

console.log(`Using API_URL: ${API_URL}`); // Verify it's loaded correctly

// Middleware to parse JSON requests
app.use(express.json());

// Serve React static files from the 'build' folder
app.use(express.static(path.join(dirname(fileURLToPath(import.meta.url)), 'build')));

// Endpoint to collect React component metrics and forward to Django
app.post('/frontend-metrics', async (req, res) => {
  const { component, value = 1 } = req.body;

  try {
    // Forward metrics to Django backend API_URL
    const response = await fetch(`${API_URL}/front_metrics`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ component, value }),
    });

    if (response.ok) {
      console.log(`Metrics recorded for component: ${component}`);
      res.status(200).json({ status: 'success' });
    } else {
      console.error('Failed to record metrics:', response.statusText);
      res.status(500).json({ error: 'Failed to record metrics' });
    }
  } catch (error) {
    console.error(`Error forwarding metrics for ${component}:`, error.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Catch-all route to serve the React app
app.get('*', (req, res) => {
  res.sendFile(path.join(dirname(fileURLToPath(import.meta.url)), 'build', 'index.html'));
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
