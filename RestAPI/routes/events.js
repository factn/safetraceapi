/*
    events are the actual rows of data
*/
const router = require('express').Router();
const EventsController = require('../controllers/events');
const checkAuth = require('../middleware/check-auth');
const rateLimiting = require('../middleware/rate-limiting');

router.get  ('/', rateLimiting(24, 100), EventsController.get_events);
router.post ('/', rateLimiting(24, 100), checkAuth, EventsController.post_event);
  
module.exports = router;