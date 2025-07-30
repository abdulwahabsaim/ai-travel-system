// AI Travel Assistant Routes
const express = require('express');
const router = express.Router();
const Itinerary = require('../models/Itinerary');
const Booking = require('../models/Booking');
const axios = require('axios');

// AI Service Configuration
const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:5001';

// Middleware to check if user is authenticated
const requireAuth = (req, res, next) => {
    if (!req.session.user) {
        return res.redirect('/auth/login');
    }
    next();
};

// AI Assistant Dashboard
router.get('/', requireAuth, async (req, res) => {
    try {
        const user = req.session.user;
        
        // Get user's recent itineraries and bookings
        const itineraries = await Itinerary.find({ user: user.id }).limit(5);
        const bookings = await Booking.find({ user: user.id }).limit(5);
        
        res.render('ai/dashboard', {
            user: user,
            itineraries: itineraries,
            bookings: bookings,
            title: 'AI Travel Assistant'
        });
    } catch (error) {
        console.error('Error loading AI dashboard:', error);
        res.status(500).render('error', { 
            error: 'Failed to load AI dashboard',
            user: req.session.user 
        });
    }
});

// AI Itinerary Generation
router.post('/generate-itinerary', requireAuth, async (req, res) => {
    try {
        const { destination, startDate, endDate, budget, travelStyle, interests, groupSize } = req.body;
        
        // Call Python AI service
        const response = await axios.post(`${AI_SERVICE_URL}/generate-itinerary`, {
            destination,
            startDate,
            endDate,
            budget: parseFloat(budget),
            travelStyle,
            interests: interests ? interests.split(',').map(i => i.trim()) : [],
            groupSize: parseInt(groupSize) || 1
        });
        
        res.json({ success: true, itinerary: response.data.itinerary });
    } catch (error) {
        console.error('Error generating itinerary:', error);
        res.status(500).json({ error: 'Failed to generate itinerary' });
    }
});

// AI Cost Predictions
router.post('/predict-costs', requireAuth, async (req, res) => {
    try {
        const { destination, duration, travelStyle, groupSize, season } = req.body;
        
        // Call Python AI service
        const response = await axios.post(`${AI_SERVICE_URL}/predict-costs`, {
            destination,
            duration: parseInt(duration),
            travelStyle,
            groupSize: parseInt(groupSize) || 1,
            season
        });
        
        res.json({ success: true, costPrediction: response.data.costPrediction });
    } catch (error) {
        console.error('Error predicting costs:', error);
        res.status(500).json({ error: 'Failed to predict costs' });
    }
});

// AI Recommendations
router.post('/get-recommendations', requireAuth, async (req, res) => {
    try {
        const { preferences, budgetRange, interests, travelHistory } = req.body;
        
        // Call Python AI service
        const response = await axios.post(`${AI_SERVICE_URL}/get-recommendations`, {
            preferences,
            budgetRange,
            interests: interests ? interests.split(',').map(i => i.trim()) : [],
            travelHistory: travelHistory ? travelHistory.split(',').map(i => i.trim()) : []
        });
        
        res.json({ success: true, recommendations: response.data.recommendations });
    } catch (error) {
        console.error('Error getting recommendations:', error);
        res.status(500).json({ error: 'Failed to get recommendations' });
    }
});

// AI Sentiment Analysis
router.post('/analyze-sentiment', requireAuth, async (req, res) => {
    try {
        const { text } = req.body;
        
        // Call Python AI service
        const response = await axios.post(`${AI_SERVICE_URL}/analyze-sentiment`, {
            text
        });
        
        res.json({ success: true, sentiment: response.data.sentiment });
    } catch (error) {
        console.error('Error analyzing sentiment:', error);
        res.status(500).json({ error: 'Failed to analyze sentiment' });
    }
});

// AI Weather Insights
router.post('/get-weather-insights', requireAuth, async (req, res) => {
    try {
        const { destination, travelDates } = req.body;
        
        // Call Python AI service
        const response = await axios.post(`${AI_SERVICE_URL}/get-weather-insights`, {
            destination,
            travelDates
        });
        
        res.json({ success: true, weatherInsights: response.data.weatherInsights });
    } catch (error) {
        console.error('Error getting weather insights:', error);
        res.status(500).json({ error: 'Failed to get weather insights' });
    }
});

// AI Translation
router.post('/translate', requireAuth, async (req, res) => {
    try {
        const { text, targetLanguage, sourceLanguage } = req.body;
        
        // Call Python AI service
        const response = await axios.post(`${AI_SERVICE_URL}/translate`, {
            text,
            targetLanguage,
            sourceLanguage: sourceLanguage || 'auto'
        });
        
        res.json({ success: true, translation: response.data.translation });
    } catch (error) {
        console.error('Error translating text:', error);
        res.status(500).json({ error: 'Failed to translate text' });
    }
});

// AI Budget Optimization
router.post('/optimize-budget', requireAuth, async (req, res) => {
    try {
        const { totalBudget, destination, duration, preferences } = req.body;
        
        // Call Python AI service
        const response = await axios.post(`${AI_SERVICE_URL}/optimize-budget`, {
            totalBudget: parseFloat(totalBudget),
            destination,
            duration: parseInt(duration),
            preferences
        });
        
        res.json({ success: true, budgetOptimization: response.data.budgetOptimization });
    } catch (error) {
        console.error('Error optimizing budget:', error);
        res.status(500).json({ error: 'Failed to optimize budget' });
    }
});

// AI Travel Tips
router.post('/generate-travel-tips', requireAuth, async (req, res) => {
    try {
        const { destination, travelStyle, interests, experienceLevel } = req.body;
        
        // Call Python AI service
        const response = await axios.post(`${AI_SERVICE_URL}/generate-travel-tips`, {
            destination,
            travelStyle,
            interests: interests ? interests.split(',').map(i => i.trim()) : [],
            experienceLevel: experienceLevel || 'intermediate'
        });
        
        res.json({ success: true, travelTips: response.data.travelTips });
    } catch (error) {
        console.error('Error generating travel tips:', error);
        res.status(500).json({ error: 'Failed to generate travel tips' });
    }
});

// Health check for AI service
router.get('/health', async (req, res) => {
    try {
        const response = await axios.get(`${AI_SERVICE_URL}/health`);
        res.json({ success: true, aiService: response.data });
    } catch (error) {
        console.error('AI service health check failed:', error);
        res.status(503).json({ 
            success: false, 
            error: 'AI service unavailable',
            message: 'The AI service is currently unavailable. Please try again later.'
        });
    }
});

module.exports = router; 