
/*
    utilities for obtaining and calculating computation IDs
*/

// function floorToTens(x) {
//     return Math.floor(x / 10) * 10;
// }
// function pad0IfBelow10 (n) {
//     return n < 10 ? `0${n}` : n;
// }
function getComputationIDOffsetByHours (offset) {
    
    
    var now = new Date();
    
    now.setUTCHours(now.getUTCHours() + offset);
    // now.setUTCMinutes(floorToTens(now.getUTCMinutes()) + offset * 10 );


    
    return `${now.getUTCHours()}-${now.getUTCMonth()}/${now.getUTCDate()}/${now.getUTCFullYear()}`;
    // return `${now.getUTCHours()}:${pad0IfBelow10(now.getUTCMinutes())}-${now.getUTCMonth()}/${now.getUTCDate()}/${now.getUTCFullYear()}`;
}

function computationID2Date (computationID) {
    let spl = computationID.split('-');
    
    let hour = Number(spl[0]);
    
    // let hour = Number(spl[0].split(':')[0]);
    // let minutes = Number(spl[0].split(':')[1]);
    
    let date = spl[1];

    let spl2 = date.split('/');
    let month = Number(spl2[0]);
    let day = Number(spl2[1]);
    let year = Number(spl2[2]);

    return new Date(Date.UTC(year, month, day, hour, 0, 0, 0));
    // return new Date(Date.UTC(year, month, day, hour, minutes, 0, 0));
}

module.exports.ComputationIDExpired = (latestExpired, check) => {
    if (check === latestExpired) 
        return true;

    return computationID2Date(check) <= computationID2Date(latestExpired);
};

module.exports.getCurrentComputationIDForClientPost = () => {
    return getComputationIDOffsetByHours(0);
};

module.exports.getCurrentComputationIDForMPCGet = () => {
    return getComputationIDOffsetByHours(-1);
};