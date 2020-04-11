
require('dotenv').config();

const express = require('express');
const app = express();

const morgan = require ('morgan');          //request logging
const bodyParser = require('body-parser');  //request body parsing
const cors = require('cors');
const helmet = require('helmet')
const compression = require('compression')

app.use (helmet())
app.use (cors());
app.use (morgan('dev'));
app.use (compression());
app.use (bodyParser.urlencoded({ extended: true }));
app.use (bodyParser.json());

//set up middleware routes
app.use('/clients', require('./routes/clients'));

app.use('/api/events', require('./routes/events'));
app.use('/api/devices', require('./routes/devices'));
app.use('/api/permissions', require('./routes/permissions'));

app.use('/api/encryption', require('./routes/encryption'));

// handle errors (if we reached this line, we havent reached a suitable route)
app.use ( (request, response, next) => {
    const error = new Error ('Not Found! :: ' + request.url);
    error.status = 404;
    //forward the error request
    next (error);
});

// catches any errors
app.use ( (error, request, response, next) => {
    response.status(error.status || 500).json({ error: error.message });
});

module.exports = app;