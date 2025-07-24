// index.js
const express = require('express');
const cors    = require('cors');
const app     = express();

// Whitelist your Netlify site for CORS
app.use(cors({
  origin: 'https://smartflow-abj.netlify.app',
  methods: ['GET','POST','OPTIONS']
}));
app.options('*', cors());
app.use(express.json());

// Predict endpoint
app.post('/predict', (req, res) => {
  // Your real prediction logic here
  const congestion = Math.floor(Math.random() * 100);
  res.json({ congestion });
});

// Admin endpoints
app.get('/admin/logs',   (req, res) => res.json({ logs: [] }));
app.post('/admin/reset', (req, res) => res.json({ reset: true }));
app.get('/admin/users',  (req, res) => res.json({ users: [] }));
app.get('/admin/status', (req, res) => res.json({ status: 'OK' }));

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`API listening on ${PORT}`));
