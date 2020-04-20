

const { db } = require('./postgresql-utils');

const AREAS_TABLE = 'areas';

/*
    OUTPUT
    {
        areas: [
            {
                area_id: integer,
                latitude: float,
                longitude: float,
                radius: integer,
            },
            { ... },
            { ... },
        ]
    }
*/
module.exports.getAreas = async (request, response, next) => {
    try {
        // get all areas and info
        const result = await db.query(`SELECT * FROM ${AREAS_TABLE};`);
        
        response.status(200).json( { 
            areas: result.rows
        } );
    }
    catch (e) { next(e); }
};