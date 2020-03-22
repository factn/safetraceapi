const express = require('express');
const app = express();

//logging
const morgan = require ('morgan');

//request body parsing
const bodyParser = require('body-parser');

// add headers before using requests to avoid CORS errors
app.use( (request, response, next) => {
    // '*' means anyone has access ( otherwise supply urls )
    response.header('Access-Control-Allow-Origin', '*');

    response.header(
        'Access-Control-Allow-Headers', 
        'Origin, X-Requested-With, Content-Type, Accept, Authorization'
    );
    
    // just querying options
    if (request.method === 'OPTIONS') {
        response.header('Access-Control-Allow-Methods', 'POST, PATCH, DELETE, GET');
        return response.status(200).json({});
    }
    next();
});

// log before using requests
app.use (morgan('dev'));

app.use (bodyParser.urlencoded({ extended: false }))
app.use (bodyParser.json());

//set up middleware routes
const mockDataRoutes = require('./routes/mockData/mockData');
app.use('/mockData', mockDataRoutes);

// const otherRoute = require('./routes/otherRoute');
// app.use('/otherRoute', otherRoute);

// handle errors (if we reached this line, we havent reached a suitable route)
app.use ( (request, response, next) => {
    
    const error = new Error ('Not Found! :: ' + request.url);
    error.status = 404;

    //forward the error request
    next (error);
});

// catches any errors
app.use ( (error, request, response, next) => {
    response.status(error.status || 500);
    response.json({ error: { message: error.message } });
});

module.exports = app;