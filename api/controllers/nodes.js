

const { db } = require('./postgresql-utils');

const NODES_TABLE = 'nodes';

/*
    OUTPUT
    {
        nodes: [
            {
                node_id: integer,
                public_key: string,
            },
            { ... },
            { ... },
        ]
    }
*/
module.exports.getNodes = async (request, response, next) => {
    try {
        
        // get all nodes and their public keys
        const result = await db.query(`SELECT * FROM ${NODES_TABLE};`);
        
        response.status(200).json( { 
            nodes: result.rows
        } );
    }
    catch (e) { next(e); }
};
