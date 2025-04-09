// src/HRCS/server.js
const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const HyperResonantCosmicShield = require('./hrcs');
const morgan = require('morgan'); // For logging requests
const helmet = require('helmet'); // For security headers
const jwt = require('jsonwebtoken'); // For JWT authentication
const bodyParser = require('body-parser'); // For parsing request bodies
const swaggerUi = require('swagger-ui-express'); // For API documentation
const swaggerJsDoc = require('swagger-jsdoc'); // For generating Swagger docs
const fs = require('fs'); // For logging to a file
const path = require('path'); // For path operations
const { body, validationResult } = require('express-validator'); // For input validation

const app = express();
const PORT = process.env.PORT || 5000;
const hrcs = new HyperResonantCosmicShield();

// Middleware
app.use(cors()); // Enable CORS
app.use(helmet()); // Set security headers
app.use(express.json()); // Parse JSON bodies
app.use(morgan('combined', { stream: fs.createWriteStream(path.join(__dirname, 'access.log'), { flags: 'a' }) })); // Log requests to a file
app.use(bodyParser.urlencoded({ extended: true })); // Parse URL-encoded bodies

// Rate limiting middleware
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
});
app.use(limiter);

// Swagger setup
const swaggerOptions = {
  swaggerDefinition: {
    openapi: '3.0.0',
    info: {
      title: 'Hyper-Resonant Cosmic Shield API',
      version: '1.0.0',
      description: 'API documentation for the HRCS project',
    },
    servers: [
      {
        url: `http://localhost:${PORT}`,
      },
    ],
  },
  apis: ['./src/CFES/server.js'], // Path to the API docs
};

const swaggerDocs = swaggerJsDoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ success: true, message: 'Server is healthy!' });
});

// Middleware for JWT authentication
const authenticateJWT = (req, res, next) => {
  const token = req.header('Authorization')?.split(' ')[1];
  if (token) {
    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
      if (err) {
        return res.sendStatus(403);
      }
      req.user = user;
      next();
    });
  } else {
    res.sendStatus(401);
  }
};

// User registration endpoint
app.post('/api/register', [
  body('username').isString().notEmpty(),
  body('password').isString().isLength({ min: 6 }),
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ success: false, errors: errors.array() });
  }

  const { username, password } = req.body;
  // Here you would save the user to the database (hashed password)
  // For demonstration, we will just return a success message
  res.json({ success: true, message: 'User  registered successfully!' });
});

// User login endpoint
app.post('/api/login', [
  body('username').isString().notEmpty(),
  body('password').isString().notEmpty(),
], (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ success: false, errors: errors.array() });
  }

  const { username, password } = req.body;
  // Here you would verify the user credentials
  // For demonstration, we will just create a token
  const token = jwt.sign({ username }, process.env.JWT_SECRET, { expiresIn: '1h' });
  res.json({ success: true, token });
});

// Endpoint to simulate activity and detect threats
app.post('/api/activity', authenticateJWT, async (req, res) => {
  const { activity } = req.body;
  try {
    hrcs.detectThreat(activity);
    res.json({ success: true, message: 'Activity processed.' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ success: false, message: 'Error processing activity.' });
  }
});

// Endpoint to encrypt data
app.post('/api/encrypt', authenticateJWT, async (req, res) => {
  const { data } = req.body;
  try {
    const encryptedData = await hrcs.encryptData(data);
    res.json({ success: true, data: encryptedData });
  } catch (error) {
    console.error(error);
    res.status(500).json({ success: false, message: 'Encryption failed.' });
  }
});

// Endpoint to decrypt data
app.post('/api/decrypt', authenticateJWT, async (req, res) => {
  const { encryptedData, iv } = req.body;
  try {
    const decryptedData = await hrcs.decryptData(encryptedData, iv);
    res.json({ success: true, data: decryptedData });
  } catch (error) {
    console.error(error);
    res.status(500).json({ success: false, message: 'Decryption failed.' });
  }
});

// Endpoint to get logged threats
app.get('/api/threats', authenticateJWT, (req, res) => {
  const threats = hrcs.getThreats();
  res.json({ success: true, threats });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ success: false, message: 'Internal Server Error' });
});

// Start the server
const server = app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

// Graceful shutdown
const shutdown = () => {
  console.log('Shutting down gracefully...');
  server.close(() => {
    console.log('Closed out remaining connections.');
    process.exit(0);
  });
};

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);
