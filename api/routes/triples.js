
const router = require('express').Router();

const TriplesController = require('../controllers/triples');

const checkAuth = require('../middleware/check-auth');

router.get ('/', checkAuth, TriplesController.getTriple);
router.post ('/', checkAuth, TriplesController.postTriple);

module.exports = router;