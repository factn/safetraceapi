const express = require('express');

const app = express();

//sets up middleware
app.use(
    (request, response, next) => {

        response.status(200).json(
            {
                message: 'Success!'
            }
        );
    }
);
module.exports = app;