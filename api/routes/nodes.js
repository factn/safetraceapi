
const router = require('express').Router();

const NodesController = require('../controllers/nodes');

const checkAuth = require('../middleware/check-auth');

router.get ('/', checkAuth, NodesController.getNodes);

module.exports = router;