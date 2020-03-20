const express = require('express');

const app = express();

const mockDataRoutes = require('./routes/mockData');

//sets up middleware
app.use('/mockData', mockDataRoutes);

// const otherRoute = require('./routes/otherRoute');
// app.use('/otherRoute', otherRoute);

module.exports = app;