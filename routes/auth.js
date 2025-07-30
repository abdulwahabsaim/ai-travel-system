const express = require('express');
const User = require('../models/User');
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

// Register page
router.get('/register', (req, res) => {
    if (req.session.user) {
        return res.redirect('/dashboard');
    }
    renderWithLayout(res, 'auth/register', { 
        title: 'Register',
        error: req.query.error,
        user: req.session.user
    });
});

// Register POST
router.post('/register', async (req, res) => {
    try {
        const { username, email, password, firstName, lastName } = req.body;
        
        // Check if user already exists
        const existingUser = await User.findOne({ 
            $or: [{ email }, { username }] 
        });
        
        if (existingUser) {
            return res.redirect('/auth/register?error=User already exists');
        }
        
        // Create new user
        const user = new User({
            username,
            email,
            password,
            firstName,
            lastName
        });
        
        await user.save();
        
        // Set session
        req.session.user = {
            id: user._id,
            username: user.username,
            email: user.email,
            firstName: user.firstName,
            lastName: user.lastName
        };
        
        res.redirect('/dashboard');
    } catch (error) {
        console.error('Registration error:', error);
        res.redirect('/auth/register?error=Registration failed');
    }
});

// Login page
router.get('/login', (req, res) => {
    if (req.session.user) {
        return res.redirect('/dashboard');
    }
    renderWithLayout(res, 'auth/login', { 
        title: 'Login',
        error: req.query.error,
        user: req.session.user
    });
});

// Login POST
router.post('/login', async (req, res) => {
    try {
        const { email, password } = req.body;
        
        // Find user
        const user = await User.findOne({ email });
        
        if (!user) {
            return res.redirect('/auth/login?error=Invalid credentials');
        }
        
        // Check password
        const isMatch = await user.comparePassword(password);
        
        if (!isMatch) {
            return res.redirect('/auth/login?error=Invalid credentials');
        }
        
        // Set session
        req.session.user = {
            id: user._id,
            username: user.username,
            email: user.email,
            firstName: user.firstName,
            lastName: user.lastName
        };
        
        res.redirect('/dashboard');
    } catch (error) {
        console.error('Login error:', error);
        res.redirect('/auth/login?error=Login failed');
    }
});

// Logout
router.get('/logout', (req, res) => {
    req.session.destroy((err) => {
        if (err) {
            console.error('Logout error:', err);
        }
        res.redirect('/');
    });
});

module.exports = router; 