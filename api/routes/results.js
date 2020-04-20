
const router = require('express').Router();

const ResultsController = require('../controllers/results');

const checkAuth = require('../middleware/check-auth');

router.get ('/', checkAuth, ResultsController.getResult);
router.post ('/', checkAuth, ResultsController.postResult);

module.exports = router;