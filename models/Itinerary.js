const mongoose = require('mongoose');

const itinerarySchema = new mongoose.Schema({
    user: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },
    title: {
        type: String,
        required: true,
        trim: true
    },
    destination: {
        type: String,
        required: true,
        trim: true
    },
    startDate: {
        type: Date,
        required: true
    },
    endDate: {
        type: Date,
        required: true
    },
    budget: {
        type: Number,
        required: true
    },
    travelStyle: {
        type: String,
        enum: ['budget', 'luxury', 'adventure', 'relaxation', 'cultural'],
        default: 'budget'
    },
    days: [{
        dayNumber: {
            type: Number,
            required: true
        },
        date: {
            type: Date,
            required: true
        },
        activities: [{
            time: {
                type: String,
                required: true
            },
            activity: {
                type: String,
                required: true
            },
            location: {
                type: String,
                required: true
            },
            description: String,
            estimatedCost: {
                type: Number,
                default: 0
            },
            bookingStatus: {
                type: String,
                enum: ['pending', 'confirmed', 'cancelled'],
                default: 'pending'
            }
        }],
        accommodation: {
            name: String,
            location: String,
            cost: Number,
            bookingStatus: {
                type: String,
                enum: ['pending', 'confirmed', 'cancelled'],
                default: 'pending'
            }
        },
        transportation: [{
            type: {
                type: String,
                enum: ['flight', 'train', 'bus', 'car', 'walking', 'public transport', 'private car', 'taxi', 'bicycle', 'hiking'],
                required: true
            },
            from: String,
            to: String,
            departureTime: String,
            arrivalTime: String,
            cost: Number,
            bookingStatus: {
                type: String,
                enum: ['pending', 'confirmed', 'cancelled'],
                default: 'pending'
            }
        }]
    }],
    totalCost: {
        type: Number,
        default: 0
    },
    aiGenerated: {
        type: Boolean,
        default: false
    },
    status: {
        type: String,
        enum: ['draft', 'confirmed', 'completed', 'cancelled'],
        default: 'draft'
    },
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

// Update the updatedAt field before saving
itinerarySchema.pre('save', function(next) {
    this.updatedAt = Date.now();
    next();
});

// Calculate total cost
itinerarySchema.methods.calculateTotalCost = function() {
    let total = 0;
    
    this.days.forEach(day => {
        // Add accommodation cost
        if (day.accommodation && day.accommodation.cost) {
            total += day.accommodation.cost;
        }
        
        // Add transportation costs
        day.transportation.forEach(transport => {
            if (transport.cost) {
                total += transport.cost;
            }
        });
        
        // Add activity costs
        day.activities.forEach(activity => {
            if (activity.estimatedCost) {
                total += activity.estimatedCost;
            }
        });
    });
    
    return total;
};

// UPDATED LINE
module.exports = mongoose.models.Itinerary || mongoose.model('Itinerary', itinerarySchema);