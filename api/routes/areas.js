
const router = require('express').Router();

const AreasController = require('../controllers/areas');

const checkAuth = require('../middleware/check-auth');

router.get ('/', checkAuth, AreasController.getAreas);

module.exports = router;