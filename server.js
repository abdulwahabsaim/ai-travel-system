const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const session = require('express-session');
const MongoStore = require('connect-mongo');
const path = require('path');
const cors = require('cors');
const ejs = require('ejs');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// MongoDB Connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/ai-travel-app', {
    useNewUrlParser: true,
    useUnifiedTopology: true
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));
db.once('open', () => {
    console.log('Connected to MongoDB');
});

// Middleware
app.use(cors());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// Session configuration
app.use(session({
    secret: process.env.SESSION_SECRET || 'your-secret-key',
    resave: false,
    saveUninitialized: false,
    store: MongoStore.create({
        mongoUrl: process.env.MONGODB_URI || 'mongodb://localhost:27017/ai-travel-app'
    }),
    cookie: {
        maxAge: 1000 * 60 * 60 * 24 // 24 hours
    }
}));

// Set EJS as templating engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Helper function to render with layout
function renderWithLayout(res, view, data) {
    ejs.renderFile(path.join(__dirname, 'views', view + '.ejs'), data, (err, content) => {
        if (err) {
            console.error('Error rendering view:', err);
            return res.status(500).send('Error rendering page');
        }
        
        ejs.renderFile(path.join(__dirname, 'views', 'layout.ejs'), {
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

// Import routes
const authRoutes = require('./routes/auth');
const itineraryRoutes = require('./routes/itinerary');
const bookingRoutes = require('./routes/booking');
const aiRoutes = require('./routes/ai');
const adminRoutes = require('./routes/admin'); // <-- IMPORT ADMIN ROUTES

// Use routes
app.use('/auth', authRoutes);
app.use('/itinerary', itineraryRoutes);
app.use('/booking', bookingRoutes);
app.use('/ai', aiRoutes);
app.use('/admin', adminRoutes); // <-- USE ADMIN ROUTES

// Home route
app.get('/', (req, res) => {
    renderWithLayout(res, 'index', { 
        user: req.session.user,
        title: 'AI Travel System'
    });
});

// Dashboard route
app.get('/dashboard', (req, res) => {
    if (!req.session.user) {
        return res.redirect('/auth/login');
    }
    renderWithLayout(res, 'dashboard', { 
        user: req.session.user,
        title: 'Dashboard'
    });
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    renderWithLayout(res, 'error', { 
        error: 'Something went wrong!',
        user: req.session.user,
        title: 'Error'
    });
});

// 404 handler
app.use((req, res) => {
    renderWithLayout(res, 'error', { 
        error: 'Page not found',
        user: req.session.user,
        title: 'Page Not Found'
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
    console.log(`Visit http://localhost:${PORT} to view the application`);
});