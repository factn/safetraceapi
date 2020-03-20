const express = require('express');

const router = express.Router();

// handle get requests
router.get('/', (request, response, next) => {
    response.status(200).json({
        message: 'Handling GET request to /mockData'
    });
});

// handle post requests
router.post('/', (request, response, next) => {

    const dataPosted = {
        id: request.body.id,
        location: request.body.location,
        timeStamp: request.body.timeStamp
    };
    response.status(201).json({
        message: 'Handling POST request to /mockData',
        createdData: dataPosted
    });
});

// {url}/mockData/{ID}
router.get ('/:ID', (request, response, next) => {
    const id = request.params.ID;
    if (id === 'special') {
        response.status(200).json({
            message: 'Special ID',
            id: id,
        });    
    }
    else {
        response.status(200).json({
            message: 'Passed in ID',
            id: id,
        });
    }
});

router.patch ('/:ID', (request, response, next) => {
    response.status(200).json({
        message: 'Updated Data',
        id: request.params.ID
    });
});

router.delete ('/:ID', (request, response, next) => {
    response.status(200).json({
        message: 'Deleted Data',
        id: request.params.ID
    });
});

module.exports = router;