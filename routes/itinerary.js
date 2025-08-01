const express = require('express');
const Itinerary = require('../models/Itinerary');
const router = express.Router();

// Helper function to render with layout
function renderWithLayout(res, view, data) {
    const ejs = require('ejs');
    const path = require('path');
    ejs.renderFile(path.join(__dirname, '..', 'views', view + '.ejs'), data, (err, content) => {
        if (err) {
            console.error('Error rendering view:', err);
            return res.status(500).send('Error rendering page');
        }
        ejs.renderFile(path.join(__dirname, '..', 'views', 'layout.ejs'), {
            ...data,
            content: content
        }, (err, html) => {
            if (err) {
                console.error('Error rendering layout:', err);
                return res.status(500).send('Error rendering page');
            }
            res.send(html);
        });
    });
}

// Middleware to check if user is authenticated
const requireAuth = (req, res, next) => {
    if (!req.session.user) {
        return res.redirect('/auth/login');
    }
    next();
};

// List all itineraries
router.get('/', requireAuth, async (req, res) => {
    try {
        const itineraries = await Itinerary.find({ user: req.session.user.id })
            .sort({ createdAt: -1 });
        renderWithLayout(res, 'itinerary/list', {
            title: 'My Itineraries',
            user: req.session.user,
            itineraries
        });
    } catch (error) {
        console.error('Error fetching itineraries:', error);
        renderWithLayout(res, 'error', {
            error: 'Failed to load itineraries',
            user: req.session.user,
            title: 'Error'
        });
    }
});

// Create new itinerary page
router.get('/create', requireAuth, (req, res) => {
    renderWithLayout(res, 'itinerary/create', {
        title: 'Create Itinerary',
        user: req.session.user
    });
});

// Create itinerary POST
router.post('/create', requireAuth, async (req, res) => {
    try {
        const { title, destination, startDate, endDate, budget, travelStyle, days, notes, aiGenerated } = req.body;

        const itineraryData = {
            user: req.session.user.id,
            title,
            destination,
            startDate,
            endDate,
            budget: parseFloat(budget),
            travelStyle,
            days: days || [],
            notes: notes || '',
            aiGenerated: aiGenerated || (days && days.length > 0)
        };

        const itinerary = new Itinerary(itineraryData);
        itinerary.totalCost = itinerary.calculateTotalCost(); // Calculate cost before saving
        await itinerary.save();

        // Handle both AJAX and form submissions
        if (req.is('application/json')) {
            return res.status(201).json({ success: true, itinerary: { _id: itinerary._id } });
        }
        
        res.redirect(`/itinerary/${itinerary._id}`);
    } catch (error) {
        console.error('Error creating itinerary:', error);
        if (req.is('application/json')) {
            return res.status(500).json({ success: false, error: 'Failed to create itinerary' });
        }
        renderWithLayout(res, 'error', {
            error: 'Failed to create itinerary',
            user: req.session.user,
            title: 'Error'
        });
    }
});

// View specific itinerary - UPDATED
router.get('/:id', requireAuth, async (req, res) => {
    try {
        const itinerary = await Itinerary.findById(req.params.id).populate('user');
        
        // Security Check: Allow owner or an admin
        if (!itinerary || (itinerary.user._id.toString() !== req.session.user.id && req.session.user.role !== 'admin')) {
            return renderWithLayout(res, 'error', {
                error: 'Itinerary not found or you do not have permission to view it.',
                user: req.session.user,
                title: 'Not Found'
            });
        }

        renderWithLayout(res, 'itinerary/view', {
            title: itinerary.title,
            user: req.session.user,
            itinerary
        });
    } catch (error) {
        console.error('Error fetching itinerary:', error);
        renderWithLayout(res, 'error', {
            error: 'Failed to load itinerary',
            user: req.session.user,
            title: 'Error'
        });
    }
});

// Edit itinerary page - UPDATED
router.get('/:id/edit', requireAuth, async (req, res) => {
    try {
        const itinerary = await Itinerary.findById(req.params.id);
        
        // Security Check: Allow owner or an admin
        if (!itinerary || (itinerary.user.toString() !== req.session.user.id && req.session.user.role !== 'admin')) {
            return renderWithLayout(res, 'error', {
                error: 'Itinerary not found or you do not have permission to edit it.',
                user: req.session.user,
                title: 'Not Found'
            });
        }
        
        renderWithLayout(res, 'itinerary/edit', {
            title: 'Edit Itinerary',
            user: req.session.user,
            itinerary
        });
    } catch (error) {
        console.error('Error fetching itinerary for edit:', error);
        renderWithLayout(res, 'error', {
            error: 'Failed to load itinerary',
            user: req.session.user,
            title: 'Error'
        });
    }
});


// Update itinerary
router.post('/:id/edit', requireAuth, async (req, res) => {
    try {
        const { title, destination, startDate, endDate, budget, travelStyle, status } = req.body;
        const itinerary = await Itinerary.findOneAndUpdate(
            { _id: req.params.id, user: req.session.user.id },
            {
                title,
                destination,
                startDate,
                endDate,
                budget: parseFloat(budget),
                travelStyle,
                status
            },
            { new: true }
        );
        if (!itinerary) {
            return renderWithLayout(res, 'error', {
                error: 'Itinerary not found',
                user: req.session.user,
                title: 'Not Found'
            });
        }
        res.redirect(`/itinerary/${itinerary._id}`);
    } catch (error) {
        console.error('Error updating itinerary:', error);
        renderWithLayout(res, 'error', {
            error: 'Failed to update itinerary',
            user: req.session.user,
            title: 'Error'
        });
    }
});

// Delete itinerary
router.post('/:id/delete', requireAuth, async (req, res) => {
    try {
        const itinerary = await Itinerary.findOneAndDelete({ 
            _id: req.params.id, 
            user: req.session.user.id 
        });
        if (!itinerary) {
            return renderWithLayout(res, 'error', {
                error: 'Itinerary not found',
                user: req.session.user,
                title: 'Not Found'
            });
        }
        res.redirect('/itinerary');
    } catch (error) {
        console.error('Error deleting itinerary:', error);
        renderWithLayout(res, 'error', {
            error: 'Failed to delete itinerary',
            user: req.session.user,
            title: 'Error'
        });
    }
});

// Add day to itinerary (API, not EJS)
router.post('/:id/days', requireAuth, async (req, res) => {
    try {
        const { dayNumber, date, activities, accommodation, transportation } = req.body;
        const itinerary = await Itinerary.findOne({ 
            _id: req.params.id, 
            user: req.session.user.id 
        });
        if (!itinerary) {
            return res.status(404).json({ error: 'Itinerary not found' });
        }
        const newDay = {
            dayNumber: parseInt(dayNumber),
            date: new Date(date),
            activities: activities || [],
            accommodation: accommodation || {},
            transportation: transportation || []
        };
        itinerary.days.push(newDay);
        itinerary.totalCost = itinerary.calculateTotalCost();
        await itinerary.save();
        res.json({ success: true, itinerary });
    } catch (error) {
        console.error('Error adding day:', error);
        res.status(500).json({ error: 'Failed to add day' });
    }
});

// API endpoint for USER-SPECIFIC stats (for dashboard)
router.get('/api/stats', requireAuth, async (req, res) => {
    try {
        const itineraryCount = await Itinerary.countDocuments({ user: req.session.user.id });
        const upcomingCount = await Itinerary.countDocuments({
            user: req.session.user.id,
            startDate: { $gte: new Date() },
            status: 'confirmed'
        });

        res.json({ success: true, itineraryCount, upcomingCount });
    } catch (error) {
        console.error('Error fetching itinerary stats:', error);
        res.status(500).json({ error: 'Failed to fetch itinerary stats' });
    }
});


// API endpoint for recent itineraries (for dashboard)
router.get('/api/recent', requireAuth, async (req, res) => {
    try {
        const itineraries = await Itinerary.find({ user: req.session.user.id })
            .sort({ createdAt: -1 })
            .limit(3)
            .select('title destination startDate endDate budget travelStyle status createdAt');
        
        res.json({ success: true, itineraries });
    } catch (error) {
        console.error('Error fetching recent itineraries:', error);
        res.status(500).json({ error: 'Failed to fetch recent itineraries' });
    }
});

module.exports = router;