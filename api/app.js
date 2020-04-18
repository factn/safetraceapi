
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
// app.use('/api/areas', require('./routes/areas'));
app.use('/api/nodes', require('./routes/nodes'));
app.use('/api/results', require('./routes/results'));
app.use('/api/shares', require('./routes/shares'));
app.use('/api/triples', require('./routes/triples'));


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