const express = require('express');
const router = express.Router();

const googleAPIUtils = require('./googleAPIUtils');

// handle get requests
router.get('/', async (request, response, next) => {
    try {
        const apiResponse = await googleAPIUtils.getDataFromSheetsAPI(request.body.rows, request.body.rangesFormat);
        response.status(200).json( apiResponse );
    }
    catch (e) { next(e); }
});

// handle post requests
router.post('/', async (request, response, next) => {
    try {
        const apiResponse = await googleAPIUtils.appendToGoogleSheet(request.body.values);
        response.status(201).json( apiResponse );
    }
    catch (e) { next(e); }
});

// handle patch requests
router.patch('/', async (request, response, next) => {
    try {
        const apiResponse = await googleAPIUtils.updateDataOnSheetsAPI(request.body.inputs);
        response.status(200).json( apiResponse );
    }
    catch (e) { next(e); }
});

// handle delete requests
router.delete ('/', async (request, response, next) => {
    try {
        const apiResponse = await googleAPIUtils.deleteDataFromSheetsAPI(request.body.rows, request.body.rangesFormat);
        response.status(200).json( apiResponse );
    }
    catch (e) { next(e); }
});

module.exports = router;