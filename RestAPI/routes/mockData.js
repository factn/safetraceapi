const express = require('express');

const router = express.Router();

const {google} = require('googleapis');


// const keys = require('./AuthKeys.json');
// const client = new google.auth.JWT(
//     keys.client_email,  // email
//     null,               // key file string
//     keys.private_key,    // key
//     ['https://www.googleapis.com/auth/spreadsheets'] // scopes
// );

const client = new google.auth.JWT(
    process.env.GS_API_CLIENT_EMAIL,  // email
    null,               // key file string
    // process.env.GS_API_PRIV_KEY,    // key
    process.env.GS_API_PRIV_KEY.replace(/\\n/gm, '\n'),

    ['https://www.googleapis.com/auth/spreadsheets'] // scopes
);



const sheetsAPI = google.sheets({version: 'v4', auth: client});

const spreadsheetId = '1Pmk1-VjxdV31aUg2XeXEaUAlrISSbkCwcOoo2ioevGI';
const sheetName = 'Data';

// columns size of the data...
const minColumn = 'A';
const maxColumn = 'B';
const dataColumns = 2;

function getRangesFromLooseIndicies(array) {
    // sort before hand
    var ranges = [], rstart, rend;
    for (var i = 0; i < array.length; i++) {
        rstart = array[i];
        rend = rstart;
        while (array[i + 1] - array[i] == 1) {
            rend = array[i + 1]; // increment the index if the numbers sequential
            i++;
        }
        ranges.push(rstart == rend ? rstart+'' : rstart + '-' + rend);
    }
    return ranges;
}

// makes sure every entry is 'x-y' format
function formatIndexToRange (i) {
    return i.includes('-') ? i : i + '-' + i;
}
// format to google sheet API range
function formatRangeToSheetRange (r) {
    r = formatIndexToRange(r);
    // split by '-'
    // +2 since row 1 is used for labels for columns (and we're using 0 based indexing...)
    let spl = r.split('-').map( ri => Number(ri) + 2 );
    return `${sheetName}!${minColumn}${spl[0]}:${maxColumn}${spl[1]}`
}

//formats it to the range notation google sheets API needs
function formatRowRangesToSheetsRanges (rowRanges) {
    return rowRanges.map((r) => formatRangeToSheetRange(r));
}

// rows =   array of indicies, 
//          or array of ranges in format [0-3, 5, 7-10]
function formatRowsInput (rows, rangesFormat) {
    if (!rangesFormat)
        rows = getRangesFromLooseIndicies(rows);
    return formatRowRangesToSheetsRanges(rows);
}
  
async function getDataFromSheetsAPI(rows, rangesFormat) {
    const apiResponse = await sheetsAPI.spreadsheets.values.batchGet({
        spreadsheetId: spreadsheetId,
        ranges: formatRowsInput (rows, rangesFormat)
    });
    
    // // or .append

    // return just an array of the table values
    return apiResponse.data.valueRanges.reduce( (a, v) => v.values ? a.concat(v.values) : a, []);
}

// handle get requests
router.get('/', async (request, response, next) => {

    try {
        // not needed ?
        // await client.authorize ((error, tokens) => {
        //     if (error)
        //         throw new Error(error);
        // });

        const apiResponse = await getDataFromSheetsAPI(request.body.rows, request.body.ranges);
        response.status(200).json( { apiResponse: apiResponse } );
    }
    catch (e) {
        next(e);
    }
});

/*
    input: array of objects, where each = 
    { 
        range: 'x-y' or 'x', 
        values: array of data entry arrays
    }
*/
async function updateDataOnSheetsAPI(inputs) {
    // format the inputs so the ranges match the sheets API ranges
    inputs.forEach( i => i.range = formatRangeToSheetRange(String(i.range)));
    
    const apiResponse = await sheetsAPI.spreadsheets.values.batchUpdate({
        spreadsheetId: spreadsheetId,
        resource: { 
            data: inputs, valueInputOption: "USER_ENTERED" 
        }
    });
    return apiResponse.data;
}

// handle patch requests
router.patch('/', async (request, response, next) => {
    try {
        const apiResponse = await updateDataOnSheetsAPI(request.body.inputs);
        response.status(200).json( { apiResponse: apiResponse } );
    }
    catch (e) {
        next(e);
    }
});


// handle post requests
// router.post('/', (request, response, next) => {

//     const dataPosted = {
//         id: request.body.id,
//         location: request.body.location,
//         timeStamp: request.body.timeStamp
//     };
//     response.status(201).json({
//         message: 'Handling POST request to /mockData',
//         createdData: dataPosted
//     });
// });


// router.delete ('/:ID', (request, response, next) => {
//     response.status(200).json({
//         message: 'Deleted Data',
//         id: request.params.ID
//     });
// });

module.exports = router;