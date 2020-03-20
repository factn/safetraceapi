const express = require('express');

const app = express();

//logging
const morgan = require ('morgan');

//request body parsing
const bodyParser = require('body-parser');

const mockDataRoutes = require('./routes/mockData');

// log before using requests
app.use(morgan('dev'));

app.use (bodyParser.urlencoded({ extended: false }))
app.use (bodyParser.json());

//sets up middleware
app.use('/mockData', mockDataRoutes);

// const otherRoute = require('./routes/otherRoute');
// app.use('/otherRoute', otherRoute);


// handle errors (if we reached this line, we havent reached a suitable route)
app.use ( (request, response, next) => {
    const error = new Error ('Not Found!');
    error.status = 404;

    //forward the error request
    next (error);
});

// catches any errors
app.use ( (error, request, response, next) => {
    response.status(error.status || 500);
    response.json({
        error: {
            message: error.message
        }
    });
});
module.exports = app;