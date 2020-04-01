/*
    events are the actual rows of data
*/
const router = require('express').Router();
const EventsController = require('../controllers/events');
const checkAuth = require('../middleware/check-auth');
const rateLimiting = require('../middleware/rate-limiting');

router.get  ('/', rateLimiting(.0001, 99999999), EventsController.get_events);
router.post ('/', rateLimiting(.0001, 99999999), checkAuth, EventsController.post_event);
  
module.exports = router;