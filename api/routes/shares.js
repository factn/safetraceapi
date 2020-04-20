
const router = require('express').Router();

const SharesController = require('../controllers/shares');

const checkAuth = require('../middleware/check-auth');

router.get ('/', checkAuth, SharesController.getShares);
router.post ('/', checkAuth, SharesController.postShares);

module.exports = router;