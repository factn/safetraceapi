const express = require('express');
const fileUpload = require('express-fileupload');
const cors = require('cors');
const bodyParser = require('body-parser');
const morgan = require('morgan');
const runSandbox = require('./run-sandbox');


const app = express();

// enable files upload
app.use(fileUpload({
    createParentPath: true,
    debug: true,
    limits: { 
        fileSize: 2 * 1024 * 1024 * 1024 //2MB max file(s) size
    },
}));

//add other middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(morgan('dev'));

app.post('/run', runSandbox);
    
//start app 
const port = process.env.PORT || 3000;
app.listen(port, () => 
    console.log(`App is listening on port ${port}.`)
);