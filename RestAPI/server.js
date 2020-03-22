require('dotenv').config();

const http = require('http');

const requestHandler = require('./app');

const server = http.createServer (requestHandler);

const port = process.env.PORT || 3000; 
server.listen(port);