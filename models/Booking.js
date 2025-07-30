const mongoose = require('mongoose');

const bookingSchema = new mongoose.Schema({
    user: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },
    itinerary: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Itinerary',
        required: true
    },
    bookingType: {
        type: String,
        enum: ['flight', 'hotel', 'activity', 'transportation', 'package'],
        required: true
    },
    provider: {
        name: {
            type: String,
            required: true
        },
        contact: {
            phone: String,
            email: String,
            website: String
        }
    },
    details: {
        from: String,
        to: String,
        departureDate: Date,
        returnDate: Date,
        departureTime: String,
        arrivalTime: String,
        duration: String,
        passengers: [{
            firstName: String,
            lastName: String,
            passportNumber: String,
            dateOfBirth: Date
        }],
        roomType: String,
        numberOfRooms: Number,
        numberOfGuests: Number,
        activityName: String,
        activityLocation: String,
        activityDuration: String
    },
    pricing: {
        basePrice: {
            type: Number,
            required: true
        },
        taxes: {
            type: Number,
            default: 0
        },
        fees: {
            type: Number,
            default: 0
        },
        totalPrice: {
            type: Number,
            required: true
        },
        currency: {
            type: String,
            default: 'USD'
        }
    },
    status: {
        type: String,
        enum: ['pending', 'confirmed', 'cancelled', 'completed'],
        default: 'pending'
    },
    paymentStatus: {
        type: String,
        enum: ['pending', 'paid', 'refunded'],
        default: 'pending'
    },
    paymentMethod: {
        type: String,
        enum: ['credit_card', 'debit_card', 'paypal', 'bank_transfer'],
        required: true
    },
    bookingReference: {
        type: String,
        unique: true,
        required: false
    },
    confirmationNumber: String,
    cancellationPolicy: String,
    refundPolicy: String,
    specialRequests: String,
    notes: String,
    createdAt: {
        type: Date,
        default: Date.now
    },
    updatedAt: {
        type: Date,
        default: Date.now
    }
});

// Generate booking reference
bookingSchema.pre('save', function(next) {
    if (!this.bookingReference) {
        this.bookingReference = 'BK' + Date.now() + Math.random().toString(36).substr(2, 5).toUpperCase();
    }
    this.updatedAt = Date.now();
    next();
});

// Calculate total price
bookingSchema.methods.calculateTotalPrice = function() {
    return this.pricing.basePrice + this.pricing.taxes + this.pricing.fees;
};

module.exports = mongoose.model('Booking', bookingSchema); 