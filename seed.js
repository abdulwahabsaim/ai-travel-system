const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
require('dotenv').config();

// Import models
const User = require('./models/User');
const Itinerary = require('./models/Itinerary');
const Booking = require('./models/Booking');

// Connect to MongoDB
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/ai-travel-app', {
    useNewUrlParser: true,
    useUnifiedTopology: true
});

const sampleData = {
    users: [
        {
            username: 'moiz',
            email: 'moiz@gmail.com',
            password: 'moiz123',
            firstName: 'Abdul',
            lastName: 'Moiz',
            role: 'admin', // The only admin
            preferences: {
                travelStyle: 'adventure',
                budget: 5000,
                preferredDestinations: ['Europe', 'Asia']
            }
        },
        {
            username: 'ali',
            email: 'ali@gmail.com',
            password: 'ali123',
            firstName: 'Ali',
            lastName: 'Arif',
            role: 'user', // Standard user
            preferences: {
                travelStyle: 'luxury',
                budget: 10000,
                preferredDestinations: ['Caribbean', 'Europe']
            }
        },
        {
            username: 'rehan',
            email: 'rehan@gmail.com',
            password: 'rehan123',
            firstName: 'Rehan',
            lastName: 'Khan',
            role: 'user', // Standard user
            preferences: {
                travelStyle: 'budget',
                budget: 2000,
                preferredDestinations: ['South America', 'Southeast Asia']
            }
        },
        {
            username: 'wahab',
            email: 'wahab@gmail.com',
            password: 'wahab123',
            firstName: 'Wahab',
            lastName: 'Saim',
            role: 'user', // Standard user
            preferences: {
                travelStyle: 'cultural',
                budget: 3500,
                preferredDestinations: ['Japan', 'Italy']
            }
        }
    ],
    
    itineraries: [
        {
            title: 'European Adventure',
            destination: 'Europe',
            startDate: new Date('2024-06-15'),
            endDate: new Date('2024-06-30'),
            budget: 5000,
            travelStyle: 'adventure',
            status: 'confirmed',
            notes: 'A 15-day adventure through Europe visiting Paris, Rome, and Barcelona',
            days: [
                {
                    dayNumber: 1,
                    date: new Date('2024-06-15'),
                    activities: [
                        {
                            time: '09:00',
                            activity: 'Eiffel Tower visit',
                            location: 'Paris, France',
                            description: 'Visit the iconic Eiffel Tower',
                            estimatedCost: 30,
                            bookingStatus: 'confirmed'
                        },
                        {
                            time: '14:00',
                            activity: 'Louvre Museum',
                            location: 'Paris, France',
                            description: 'Explore the world-famous art museum',
                            estimatedCost: 20,
                            bookingStatus: 'confirmed'
                        }
                    ],
                    accommodation: {
                        name: 'Hotel Paris',
                        location: 'Paris, France',
                        cost: 150,
                        bookingStatus: 'confirmed'
                    },
                    transportation: [
                        {
                            type: 'train',
                            from: 'Airport',
                            to: 'Paris Center',
                            departureTime: '08:00',
                            arrivalTime: '08:30',
                            cost: 25,
                            bookingStatus: 'confirmed'
                        }
                    ]
                }
            ]
        },
        {
            title: 'Caribbean Paradise',
            destination: 'Caribbean',
            startDate: new Date('2024-08-10'),
            endDate: new Date('2024-08-20'),
            budget: 8000,
            travelStyle: 'luxury',
            status: 'confirmed',
            notes: 'A luxurious 10-day Caribbean cruise with beach activities',
            days: [
                {
                    dayNumber: 1,
                    date: new Date('2024-08-10'),
                    activities: [
                        {
                            time: '10:00',
                            activity: 'Beach relaxation',
                            location: 'Caribbean Beach',
                            description: 'Relax on pristine beaches',
                            estimatedCost: 0,
                            bookingStatus: 'confirmed'
                        },
                        {
                            time: '15:00',
                            activity: 'Snorkeling',
                            location: 'Coral Reef',
                            description: 'Explore underwater marine life',
                            estimatedCost: 80,
                            bookingStatus: 'confirmed'
                        }
                    ],
                    accommodation: {
                        name: 'Luxury Resort',
                        location: 'Caribbean Island',
                        cost: 400,
                        bookingStatus: 'confirmed'
                    },
                    transportation: [
                        {
                            type: 'flight',
                            from: 'Miami',
                            to: 'Caribbean',
                            departureTime: '09:00',
                            arrivalTime: '11:00',
                            cost: 300,
                            bookingStatus: 'confirmed'
                        }
                    ]
                }
            ]
        },
        {
            title: 'Tokyo Exploration',
            destination: 'Japan',
            startDate: new Date('2024-09-05'),
            endDate: new Date('2024-09-15'),
            budget: 6000,
            travelStyle: 'cultural',
            status: 'draft',
            notes: 'A 10-day cultural exploration of Tokyo and surrounding areas',
            days: [
                {
                    dayNumber: 1,
                    date: new Date('2024-09-05'),
                    activities: [
                        {
                            time: '08:00',
                            activity: 'Senso-ji Temple',
                            location: 'Tokyo, Japan',
                            description: 'Visit the oldest temple in Tokyo',
                            estimatedCost: 0,
                            bookingStatus: 'pending'
                        },
                        {
                            time: '14:00',
                            activity: 'Tokyo Skytree',
                            location: 'Tokyo, Japan',
                            description: 'Visit the tallest tower in Japan',
                            estimatedCost: 25,
                            bookingStatus: 'pending'
                        }
                    ],
                    accommodation: {
                        name: 'Modern Hotel',
                        location: 'Shibuya, Tokyo',
                        cost: 200,
                        bookingStatus: 'pending'
                    },
                    transportation: [
                        {
                            type: 'train',
                            from: 'Airport',
                            to: 'Shibuya',
                            departureTime: '07:00',
                            arrivalTime: '07:45',
                            cost: 15,
                            bookingStatus: 'confirmed'
                        }
                    ]
                }
            ]
        }
    ],
    
    bookings: [
        {
            bookingType: 'flight',
            provider: {
                name: 'Delta Airlines',
                contact: {
                    phone: '+1-800-221-1212',
                    email: 'support@delta.com',
                    website: 'www.delta.com'
                }
            },
            details: {
                flightNumber: 'DL123',
                departure: 'JFK',
                arrival: 'CDG',
                departureTime: new Date('2024-06-15T10:00:00Z'),
                arrivalTime: new Date('2024-06-15T22:00:00Z'),
                class: 'Economy'
            },
            pricing: {
                basePrice: 800,
                taxes: 100,
                fees: 50,
                totalPrice: 950
            },
            status: 'confirmed',
            paymentStatus: 'paid',
            paymentMethod: 'credit_card'
        },
        {
            bookingType: 'hotel',
            provider: {
                name: 'Hilton Paris',
                contact: {
                    phone: '+33-1-42-56-56-56',
                    email: 'reservations@hilton-paris.com',
                    website: 'www.hilton.com/paris'
                }
            },
            details: {
                checkIn: new Date('2024-06-15'),
                checkOut: new Date('2024-06-20'),
                roomType: 'Standard Double',
                guests: 2,
                amenities: ['WiFi', 'Breakfast', 'Gym']
            },
            pricing: {
                basePrice: 1200,
                taxes: 180,
                fees: 0,
                totalPrice: 1380
            },
            status: 'confirmed',
            paymentStatus: 'paid',
            paymentMethod: 'credit_card'
        },
        {
            bookingType: 'activity',
            provider: {
                name: 'Paris Tours Co.',
                contact: {
                    phone: '+33-1-40-20-30-40',
                    email: 'info@paristours.com',
                    website: 'www.paristours.com'
                }
            },
            details: {
                activityName: 'Eiffel Tower Skip-the-Line Tour',
                date: new Date('2024-06-16'),
                duration: '3 hours',
                participants: 2,
                meetingPoint: 'Eiffel Tower entrance'
            },
            pricing: {
                basePrice: 120,
                taxes: 0,
                fees: 10,
                totalPrice: 130
            },
            status: 'confirmed',
            paymentStatus: 'paid',
            paymentMethod: 'paypal'
        },
        {
            bookingType: 'transportation',
            provider: {
                name: 'Royal Caribbean',
                contact: {
                    phone: '+1-866-562-7625',
                    email: 'bookings@royalcaribbean.com',
                    website: 'www.royalcaribbean.com'
                }
            },
            details: {
                from: 'Miami',
                to: 'Caribbean Islands',
                departureDate: new Date('2024-08-10'),
                returnDate: new Date('2024-08-20'),
                departureTime: '16:00',
                arrivalTime: '08:00',
                duration: '10 days'
            },
            pricing: {
                basePrice: 3000,
                taxes: 300,
                fees: 200,
                totalPrice: 3500
            },
            status: 'confirmed',
            paymentStatus: 'paid',
            paymentMethod: 'credit_card'
        }
    ]
};

async function seedDatabase() {
    try {
        console.log('🌱 Starting database seeding...');
        
        // Clear existing data
        await User.deleteMany({});
        await Itinerary.deleteMany({});
        await Booking.deleteMany({});
        console.log('🗑️  Cleared existing data');
        
        // Create users
        const createdUsers = [];
        for (const userData of sampleData.users) {
            const user = new User({
                ...userData,
                password: userData.password // Let the User model hash it automatically
            });
            const savedUser = await user.save();
            createdUsers.push(savedUser);
            console.log(`👤 Created user: ${userData.username}`);
        }
        
        // Create itineraries and associate with users
        const createdItineraries = [];
        for (let i = 0; i < sampleData.itineraries.length; i++) {
            const itineraryData = sampleData.itineraries[i];
            const user = createdUsers[i % createdUsers.length]; // Distribute itineraries among users
            
            const itinerary = new Itinerary({
                ...itineraryData,
                user: user._id
            });
            const savedItinerary = await itinerary.save();
            createdItineraries.push(savedItinerary);
            console.log(`🗺️  Created itinerary: ${itineraryData.title}`);
        }
        
        // Create bookings and associate with users and itineraries
        for (let i = 0; i < sampleData.bookings.length; i++) {
            const bookingData = sampleData.bookings[i];
            const user = createdUsers[i % createdUsers.length]; // Distribute bookings among users
            const itinerary = createdItineraries[i % createdItineraries.length]; // Associate with itineraries
            
            const booking = new Booking({
                ...bookingData,
                user: user._id,
                itinerary: itinerary._id
            });
            await booking.save();
            console.log(`📅 Created booking: ${bookingData.bookingType} - ${bookingData.provider.name}`);
        }
        
        console.log('\n✅ Database seeding completed successfully!');
        console.log(`📊 Created ${createdUsers.length} users, ${createdItineraries.length} itineraries, and ${sampleData.bookings.length} bookings`);
        console.log('\n🔑 Test Login Credentials:');
        console.log('Admin Email: moiz@gmail.com, Password: moiz123');
        console.log('User Email: ali@gmail.com, Password: ali123');
        console.log('User Email: rehan@gmail.com, Password: rehan123');
        console.log('User Email: wahab@gmail.com, Password: wahab123');
        console.log('\n🚀 You can now test the application with this sample data!');
        
    } catch (error) {
        console.error('❌ Error seeding database:', error);
    } finally {
        mongoose.connection.close();
        console.log('🔌 Database connection closed');
    }
}

// Run the seed function
seedDatabase();