const express = require('express');
const mongoose = require('mongoose'); // <-- ADD THIS LINE
const Booking = require('../models/Booking');
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

// List all bookings
router.get('/', requireAuth, async (req, res) => {
    try {
        const bookings = await Booking.find({ user: req.session.user.id })
            .populate('itinerary')
            .sort({ createdAt: -1 });
        renderWithLayout(res, 'booking/list', {
            title: 'My Bookings',
            user: req.session.user,
            bookings
        });
    } catch (error) {
        console.error('Error fetching bookings:', error);
        renderWithLayout(res, 'error', {
            error: 'Failed to load bookings',
            user: req.session.user,
            title: 'Error'
        });
    }
});

// Create new booking page
router.get('/create', requireAuth, async (req, res) => {
    try {
        const itineraries = await Itinerary.find({ user: req.session.user.id });
        renderWithLayout(res, 'booking/create', {
            title: 'Create Booking',
            user: req.session.user,
            itineraries
        });
    } catch (error) {
        console.error('Error loading create booking page:', error);
        renderWithLayout(res, 'error', {
            error: 'Failed to load booking form',
            user: req.session.user,
            title: 'Error'
        });
    }
});

// Create booking POST
router.post('/create', requireAuth, async (req, res) => {
    try {
        const {
            itineraryId,
            bookingType,
            providerName,
            providerPhone,
            providerEmail,
            providerWebsite,
            from,
            to,
            departureDate,
            returnDate,
            departureTime,
            arrivalTime,
            duration,
            basePrice,
            taxes,
            fees,
            paymentMethod,
            specialRequests
        } = req.body;
        const booking = new Booking({
            user: req.session.user.id,
            itinerary: itineraryId,
            bookingType,
            provider: {
                name: providerName,
                contact: {
                    phone: providerPhone,
                    email: providerEmail,
                    website: providerWebsite
                }
            },
            details: {
                from,
                to,
                departureDate: departureDate ? new Date(departureDate) : null,
                returnDate: returnDate ? new Date(returnDate) : null,
                departureTime,
                arrivalTime,
                duration
            },
            pricing: {
                basePrice: parseFloat(basePrice),
                taxes: parseFloat(taxes) || 0,
                fees: parseFloat(fees) || 0,
                totalPrice: parseFloat(basePrice) + (parseFloat(taxes) || 0) + (parseFloat(fees) || 0)
            },
            paymentMethod,
            specialRequests
        });
        await booking.save();
        res.redirect(`/booking/${booking._id}`);
    } catch (error) {
        console.error('Error creating booking:', error);
        renderWithLayout(res, 'error', {
            error: 'Failed to create booking',
            user: req.session.user,
            title: 'Error'
        });
    }
});

// View specific booking - UPDATED
router.get('/:id', requireAuth, async (req, res) => {
    try {
        const booking = await Booking.findById(req.params.id).populate('itinerary');
        
        // Security Check: Allow owner or an admin
        if (!booking || (booking.user.toString() !== req.session.user.id && req.session.user.role !== 'admin')) {
            return renderWithLayout(res, 'error', {
                error: 'Booking not found or you do not have permission to view it.',
                user: req.session.user,
                title: 'Not Found'
            });
        }

        renderWithLayout(res, 'booking/view', {
            title: 'Booking Details',
            user: req.session.user,
            booking
        });
    } catch (error) {
        console.error('Error fetching booking:', error);
        renderWithLayout(res, 'error', {
            error: 'Failed to load booking',
            user: req.session.user,
            title: 'Error'
        });
    }
});

// Edit booking page - UPDATED
router.get('/:id/edit', requireAuth, async (req, res) => {
    try {
        const booking = await Booking.findById(req.params.id).populate('itinerary');
        
        // Security Check: Allow owner or an admin
        if (!booking || (booking.user.toString() !== req.session.user.id && req.session.user.role !== 'admin')) {
            return renderWithLayout(res, 'error', {
                error: 'Booking not found or you do not have permission to edit it.',
                user: req.session.user,
                title: 'Not Found'
            });
        }

        const itineraries = await Itinerary.find({ user: req.session.user.id });
        renderWithLayout(res, 'booking/edit', {
            title: 'Edit Booking',
            user: req.session.user,
            booking,
            itineraries
        });
    } catch (error) {
        console.error('Error fetching booking for edit:', error);
        renderWithLayout(res, 'error', {
            error: 'Failed to load booking',
            user: req.session.user,
            title: 'Error'
        });
    }
});


// Update booking
router.post('/:id/edit', requireAuth, async (req, res) => {
    try {
        const {
            itineraryId,
            bookingType,
            providerName,
            providerPhone,
            providerEmail,
            providerWebsite,
            from,
            to,
            departureDate,
            returnDate,
            departureTime,
            arrivalTime,
            duration,
            basePrice,
            taxes,
            fees,
            paymentMethod,
            status,
            paymentStatus,
            specialRequests
        } = req.body;
        const booking = await Booking.findOneAndUpdate(
            { _id: req.params.id, user: req.session.user.id },
            {
                itinerary: itineraryId,
                bookingType,
                provider: {
                    name: providerName,
                    contact: {
                        phone: providerPhone,
                        email: providerEmail,
                        website: providerWebsite
                    }
                },
                details: {
                    from,
                    to,
                    departureDate: departureDate ? new Date(departureDate) : null,
                    returnDate: returnDate ? new Date(returnDate) : null,
                    departureTime,
                    arrivalTime,
                    duration
                },
                pricing: {
                    basePrice: parseFloat(basePrice),
                    taxes: parseFloat(taxes) || 0,
                    fees: parseFloat(fees) || 0,
                    totalPrice: parseFloat(basePrice) + (parseFloat(taxes) || 0) + (parseFloat(fees) || 0)
                },
                paymentMethod,
                status,
                paymentStatus,
                specialRequests
            },
            { new: true }
        );
        if (!booking) {
            return renderWithLayout(res, 'error', {
                error: 'Booking not found',
                user: req.session.user,
                title: 'Not Found'
            });
        }
        res.redirect(`/booking/${booking._id}`);
    } catch (error) {
        console.error('Error updating booking:', error);
        renderWithLayout(res, 'error', {
            error: 'Failed to update booking',
            user: req.session.user,
            title: 'Error'
        });
    }
});

// Delete booking
router.post('/:id/delete', requireAuth, async (req, res) => {
    try {
        const booking = await Booking.findOneAndDelete({ 
            _id: req.params.id, 
            user: req.session.user.id 
        });
        if (!booking) {
            return renderWithLayout(res, 'error', {
                error: 'Booking not found',
                user: req.session.user,
                title: 'Not Found'
            });
        }
        res.redirect('/booking');
    } catch (error) {
        console.error('Error deleting booking:', error);
        renderWithLayout(res, 'error', {
            error: 'Failed to delete booking',
            user: req.session.user,
            title: 'Error'
        });
    }
});

// Update booking status (API, not EJS)
router.post('/:id/status', requireAuth, async (req, res) => {
    try {
        const { status, paymentStatus } = req.body;
        const booking = await Booking.findOneAndUpdate(
            { _id: req.params.id, user: req.session.user.id },
            { status, paymentStatus },
            { new: true }
        );
        if (!booking) {
            return res.status(404).json({ error: 'Booking not found' });
        }
        res.json({ success: true, booking });
    } catch (error) {
        console.error('Error updating booking status:', error);
        res.status(500).json({ error: 'Failed to update booking status' });
    }
});

// API endpoint for USER-SPECIFIC stats (for dashboard)
router.get('/api/stats', requireAuth, async (req, res) => {
    try {
        const bookingStats = await Booking.aggregate([
            { $match: { user: new mongoose.Types.ObjectId(req.session.user.id) } },
            {
                $group: {
                    _id: null,
                    bookingCount: { $sum: 1 },
                    totalSpent: { $sum: "$pricing.totalPrice" }
                }
            }
        ]);

        const stats = bookingStats[0] || { bookingCount: 0, totalSpent: 0 };
        res.json({ success: true, ...stats });

    } catch (error) {
        console.error('Error fetching booking stats:', error);
        res.status(500).json({ error: 'Failed to fetch booking stats' });
    }
});

// API endpoint for recent bookings (for dashboard)
router.get('/api/recent', requireAuth, async (req, res) => {
    try {
        const bookings = await Booking.find({ user: req.session.user.id })
            .populate('itinerary', 'title destination')
            .sort({ createdAt: -1 })
            .limit(3)
            .select('bookingType provider details pricing status paymentStatus createdAt');
        
        res.json({ success: true, bookings });
    } catch (error) {
        console.error('Error fetching recent bookings:', error);
        res.status(500).json({ error: 'Failed to fetch recent bookings' });
    }
});

module.exports = router;