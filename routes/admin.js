const express = require('express');
const router = express.Router();
const User = require('../models/User');
const Itinerary = require('../models/Itinerary');
const Booking = require('../models/Booking');

// Middleware to check if user is authenticated and is an admin
const requireAdmin = (req, res, next) => {
    if (req.session.user && req.session.user.role === 'admin') {
        next();
    } else {
        res.status(403).send('Forbidden: Access is denied');
    }
};

// Apply admin middleware to all routes in this file
router.use(requireAdmin);

// Helper function to render admin views with layout
function renderAdminLayout(res, view, data) {
    const ejs = require('ejs');
    const path = require('path');
    
    ejs.renderFile(path.join(__dirname, '..', 'views', view + '.ejs'), data, (err, content) => {
        if (err) {
            console.error('Error rendering admin view:', err);
            return res.status(500).send('Error rendering page');
        }
        
        ejs.renderFile(path.join(__dirname, '..', 'views', 'layout.ejs'), {
            ...data,
            content: content
        }, (err, html) => {
            if (err) {
                console.error('Error rendering admin layout:', err);
                return res.status(500).send('Error rendering page');
            }
            res.send(html);
        });
    });
}

// Admin Dashboard
router.get('/', async (req, res) => {
    try {
        const userCount = await User.countDocuments();
        const itineraryCount = await Itinerary.countDocuments();
        const bookingCount = await Booking.countDocuments();
        
        renderAdminLayout(res, 'admin/dashboard', {
            title: 'Admin Dashboard',
            user: req.session.user,
            stats: { userCount, itineraryCount, bookingCount }
        });
    } catch (error) {
        console.error('Error loading admin dashboard:', error);
        res.status(500).send("Error loading admin dashboard");
    }
});

// Manage Users
router.get('/users', async (req, res) => {
    try {
        const users = await User.find().sort({ createdAt: -1 });
        renderAdminLayout(res, 'admin/users', {
            title: 'Manage Users',
            user: req.session.user,
            users
        });
    } catch (error) {
        console.error('Error fetching users:', error);
        res.status(500).send("Error fetching users");
    }
});

// Manage All Itineraries
router.get('/itineraries', async (req, res) => {
    try {
        const itineraries = await Itinerary.find().populate('user', 'username email').sort({ createdAt: -1 });
        renderAdminLayout(res, 'admin/itineraries', {
            title: 'Manage Itineraries',
            user: req.session.user,
            itineraries
        });
    } catch (error) {
        console.error('Error fetching itineraries:', error);
        res.status(500).send("Error fetching itineraries");
    }
});

// Manage All Bookings
router.get('/bookings', async (req, res) => {
    try {
        const bookings = await Booking.find().populate('user', 'username email').sort({ createdAt: -1 });
        renderAdminLayout(res, 'admin/bookings', {
            title: 'Manage Bookings',
            user: req.session.user,
            bookings
        });
    } catch (error) {
        console.error('Error fetching bookings:', error);
        res.status(500).send("Error fetching bookings");
    }
});

module.exports = router;