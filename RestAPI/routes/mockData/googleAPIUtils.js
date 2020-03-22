const {google} = require('googleapis');

const client = new google.auth.JWT(
    process.env.GS_API_CLIENT_EMAIL,                    // email
    null,                                               // key file string
    process.env.GS_API_PRIV_KEY.replace(/\\n/gm, '\n'), // key
    ['https://www.googleapis.com/auth/spreadsheets']    // scopes
);

const sheetsAPI = google.sheets({version: 'v4', auth: client});

const spreadsheetId = '1Pmk1-VjxdV31aUg2XeXEaUAlrISSbkCwcOoo2ioevGI';
const sheetName = 'Data';

// columns size of the data...
const minColumn = 'A';
const maxColumn = 'B';
const dataColumns = 2;

// translates array of integer indicies into string ranges
// [0,1,2,5,7,8,9] => ["0-2", "5", "7-9"]
function getRangesFromLooseIndicies (array) {
    let ranges = [], rstart, rend;
    for (let i = 0; i < array.length; i++) {
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

// makes sure entry is 'x-y' format
function formatIndexToRange (i) {
    return i.includes('-') ? i : i + '-' + i;
}
// format to google sheet API range
function formatToSheetsAPIRange (r) {
    r = formatIndexToRange(String(r));
    // split by '-'
    // +2 since row 1 is used for labels for columns (and we're using 0 based indexing...)
    let spl = r.split('-').map( ri => Number(ri) + 2 );
    return `${sheetName}!${minColumn}${spl[0]}:${maxColumn}${spl[1]}`
}

// rows =   array of indicies, 
//          or array of ranges in format [0-3, 5, 7-10]
function formatRowsInput (rows, rangesFormat, debug) {
    // make sure it's in a string range format
    if (!rangesFormat)
        rows = getRangesFromLooseIndicies(rows);

    debug.value = rows.join(',');

    //formats it to the range notation google sheets API needs
    return rows.map(r => formatToSheetsAPIRange(r));
}
      
module.exports = {
    getDataFromSheetsAPI: async function (rows, rangesFormat) {
        const response = await sheetsAPI.spreadsheets.values.batchGet({
            spreadsheetId: spreadsheetId,
            ranges: formatRowsInput (rows, rangesFormat, {})
        });
        // return just an array of the table values
        let respArray = response.data.valueRanges.reduce( (a, v) => v.values ? a.concat(v.values) : a, []);
        return { response: respArray, statusText: response.statusText };
    },
    
    /*
        input: array of objects, where each = 
        { 
            range: 'x-y' or 'x', 
            values: array of data entry arrays
        }
    */
    updateDataOnSheetsAPI: async function(inputs) {
        // format the inputs so the ranges match the sheets API ranges
        inputs.forEach( i => i.range = formatToSheetsAPIRange(i.range));
        
        const response = await sheetsAPI.spreadsheets.values.batchUpdate({
            spreadsheetId: spreadsheetId,
            resource: { data: inputs, valueInputOption: "USER_ENTERED" }
        });
        return { response: response.data, message: response.statusText };
    },
    
    /*
        values = array of data value arrays
    */
    appendToGoogleSheet: async function (values) {
        const response = await sheetsAPI.spreadsheets.values.append({
            spreadsheetId: spreadsheetId,
            range: sheetName,
            valueInputOption: 'USER_ENTERED',
            resource: { values: values },
        });
        return { response: response.data, message: response.statusText };
    },
    
    deleteDataFromSheetsAPI: async function(rows, rangesFormat) {
        let debug = {};
        const response = await sheetsAPI.spreadsheets.values.batchClear({
            spreadsheetId: spreadsheetId,
            ranges: formatRowsInput (rows, rangesFormat, debug)
        });
        return { response: response.data, statusText: `Deleted Entries: ${debug.value} :: [${response.statusText}]` };
    },
};