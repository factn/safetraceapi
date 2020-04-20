

const { db } = require('./postgresql-utils');
const { assertBodyKey, assertHeaderKey } = require('./controller-utils');
const ComputationIDs = require('./computation-id');

const SHARES = 'shares';
const NODE_ID = 'node_id';
const SHARE = 'share';

const AREA_ID = 'area_id';

const COMPUTATION_ID = 'computation_id';

const SHARES_TABLE = 'shares';
const RESULTS_TABLE = 'results';

const NODES_COUNT = 3;

/*
    n = 2t + 1
    t = (n - 1) / 2
    min responses = t + 1 = ((n - 1) / 2) + 1
*/
const MIN_RESPONSES = ((NODES_COUNT - 1) / 2) + 1;

/*
    REQUEST {
        node_id: integer,
        computation_id: string,
        shares: [
            {
                area_id: integer,
                share: string
            },
            { ... },
            { ... },
        ]
    }
*/
module.exports.postResult = async (request, response, next) => {
    try {
        // assert the request body is in the right format
        const action = 'Post Results';
        let node_id = assertBodyKey (request.body, NODE_ID, action);
        let computation_id = assertBodyKey (request.body, COMPUTATION_ID, action);
        
        let shares = assertBodyKey (request.body, SHARES, action);
        if (!Array.isArray(shares)) 
            throw new Error(`Error! [${action}]: ${SHARES} key must be an array`);
        
        for (let i = 0; i < shares.length; i++) {
            assertBodyKey (shares[i], AREA_ID, action);
            assertBodyKey (shares[i], SHARE, action);
        }

        // sql list of values to add
        let valuesSQL = shares.map( (s) => `('${computation_id}', ${node_id}, ${s[AREA_ID]}, '${s[SHARE]}')` ).join (', ');
        
        // add the result shares to the DB
        await db.query(`INSERT INTO ${RESULTS_TABLE} (${COMPUTATION_ID}, ${NODE_ID}, ${AREA_ID}, ${SHARE}) VALUES ${valuesSQL};`);
        
        // chekc if computation id is expired (this assumes we get MPC response with all areas calculated)
        const resultsWithComputationID = await db.query(`SELECT ${NODE_ID} FROM ${RESULTS_TABLE} WHERE ${COMPUTATION_ID} = '${computation_id}';`);
        
        // get a list of node id's that have completed this computation id ( Set ( array ) removes duplicates )
        const nodeIDsCompletedComputations = [ ...new Set(resultsWithComputationID.rows.map( r => r[NODE_ID] )) ];

        // computation is done and expired
        if (nodeIDsCompletedComputations.length >= MIN_RESPONSES) {

            // delete the shares with the current expired computation id
            await db.query(`DELETE FROM ${SHARES_TABLE} WHERE ${COMPUTATION_ID} = '${computation_id}';`);

            // get the computation id's included in all lefotver shares
            const computationIDsFromAllShares = await db.query(`SELECT ${COMPUTATION_ID} FROM ${SHARES_TABLE};`);

            // get a list of all the computation IDs that are in the shares table
            const allComputationIDsInShares = [ ...new Set( computationIDsFromAllShares.rows.map( r => r[COMPUTATION_ID] ) ) ];

            // filter to only get the expired ones.
            const expiredComputationIDs = allComputationIDsInShares.filter( c => ComputationIDs.ComputationIDExpired(computation_id, c) );

            if (expiredComputationIDs.length > 0) {

                // join into a comma seperated string with single quotes around the id (for the SQL query)
                const expiredComputationIDsSQL = expiredComputationIDs.map( cid => `'${cid}'` ).join(', ');
                
                // delete any rows in the shares table that have an expired computation id
                await db.query(`DELETE FROM ${SHARES_TABLE} WHERE ${COMPUTATION_ID} IN (${expiredComputationIDsSQL});`);
            }
        }

        response.status(201).json( { 
            status: "OK"
        } );
    }
    catch (e) { next(e); }
};


/*
    REQUEST
    {
        computation_id: string [ hour-month/day/year ]
    }
    OUTPUT
    {
        shares: [
            {
                node_id: integer,
                area_id: integer,
                share: string
            },
            { ... },
            { ... },
        ]
    }
*/
module.exports.getResult = async (request, response, next) => {
    try {
        const action = 'Get Results';
        let computation_id = assertBodyKey (request.body, COMPUTATION_ID, action);

        const result = await db.query(`SELECT ${NODE_ID}, ${AREA_ID}, ${SHARE} FROM ${RESULTS_TABLE} WHERE ${COMPUTATION_ID} = '${computation_id}';`);
        
        response.status(200).json( { 
            shares: result.rows
        } );
    }
    catch (e) { next(e); }
};
