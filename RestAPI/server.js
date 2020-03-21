require('dotenv').config();

// console.log(process.env);

const http = require('http');

const requestHandler = require('./app');
// use 3000 as default port
const port = process.env.PORT || 3000; 

const server = http.createServer (requestHandler);


server.listen(port);