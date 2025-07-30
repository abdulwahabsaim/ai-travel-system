# AI Travel Service

A Python-based AI service that provides intelligent travel planning features for the AI Travel System.

## Features

### 🤖 AI-Powered Modules

1. **Itinerary Generator**
   - Creates personalized travel itineraries
   - Considers travel style, budget, and interests
   - Generates daily activities and recommendations

2. **Cost Predictor**
   - Predicts travel costs for destinations
   - Considers seasonal factors and travel style
   - Provides budget optimization recommendations

3. **Recommendation Engine**
   - Personalized destination recommendations
   - Based on user preferences and travel history
   - Alternative recommendations for different criteria

4. **Sentiment Analyzer**
   - Analyzes travel reviews and feedback
   - Provides sentiment scores and insights
   - Travel-specific keyword analysis

5. **Weather Analyzer**
   - Weather insights for travel planning
   - Seasonal recommendations and forecasts
   - Packing and activity suggestions

6. **Translation Service**
   - Text translation for international travel
   - Essential phrases for destinations
   - Language detection and pronunciation guides

## Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Navigate to the AI service directory:**
   ```bash
   cd ai_service
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the service:**
   ```bash
   python app.py
   ```

   Or use the batch file on Windows:
   ```bash
   start_ai_service.bat
   ```

The service will start on `http://localhost:5001`

## API Endpoints

### Health Check
- **GET** `/health` - Service health status

### Itinerary Generation
- **POST** `/generate-itinerary` - Generate AI-powered travel itinerary
- **POST** `/generate-travel-tips` - Generate personalized travel tips

### Cost Prediction
- **POST** `/predict-costs` - Predict travel costs for destination
- **POST** `/optimize-budget` - Optimize budget allocation

### Recommendations
- **POST** `/get-recommendations` - Get personalized travel recommendations

### Sentiment Analysis
- **POST** `/analyze-sentiment` - Analyze sentiment of travel reviews

### Weather Insights
- **POST** `/get-weather-insights` - Get weather insights for travel planning

### Translation
- **POST** `/translate` - Translate text for international travel

## API Usage Examples

### Generate Itinerary
```bash
curl -X POST http://localhost:5001/generate-itinerary \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Paris",
    "startDate": "2024-06-15",
    "endDate": "2024-06-20",
    "budget": 3000,
    "travelStyle": "cultural",
    "interests": ["museums", "food"],
    "groupSize": 2
  }'
```

### Predict Costs
```bash
curl -X POST http://localhost:5001/predict-costs \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Tokyo",
    "duration": 7,
    "travelStyle": "balanced",
    "groupSize": 2,
    "season": "spring"
  }'
```

### Get Recommendations
```bash
curl -X POST http://localhost:5001/get-recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "preferences": {
      "travelStyle": "adventure",
      "costLevel": "medium"
    },
    "budgetRange": {
      "min": 2000,
      "max": 5000
    },
    "interests": ["nature", "culture"],
    "travelHistory": ["Paris", "London"]
  }'
```

### Analyze Sentiment
```bash
curl -X POST http://localhost:5001/analyze-sentiment \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The hotel was amazing with excellent service and great location!"
  }'
```

### Get Weather Insights
```bash
curl -X POST http://localhost:5001/get-weather-insights \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Bali",
    "travelDates": {
      "start": "2024-08-01",
      "end": "2024-08-07"
    }
  }'
```

### Translate Text
```bash
curl -X POST http://localhost:5001/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, how are you?",
    "targetLanguage": "spanish",
    "sourceLanguage": "english"
  }'
```

## Integration with Node.js Application

The AI service is designed to work alongside the Node.js travel application. The Node.js app can make HTTP requests to these endpoints to get AI-powered features.

### Example Integration in Node.js

```javascript
const axios = require('axios');

// Generate itinerary
async function generateItinerary(params) {
  try {
    const response = await axios.post('http://localhost:5001/generate-itinerary', params);
    return response.data;
  } catch (error) {
    console.error('Error generating itinerary:', error);
    throw error;
  }
}

// Predict costs
async function predictCosts(params) {
  try {
    const response = await axios.post('http://localhost:5001/predict-costs', params);
    return response.data;
  } catch (error) {
    console.error('Error predicting costs:', error);
    throw error;
  }
}
```

## Configuration

The service uses environment variables for configuration. Create a `.env` file in the `ai_service` directory:

```env
# Service Configuration
PORT=5001
DEBUG=True

# Optional: External API Keys (for future enhancements)
# OPENAI_API_KEY=your-openai-api-key
# WEATHER_API_KEY=your-weather-api-key
# TRANSLATION_API_KEY=your-translation-api-key
```

## Development

### Project Structure
```
ai_service/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── ai_modules/           # AI modules package
│   ├── __init__.py
│   ├── itinerary_generator.py
│   ├── cost_predictor.py
│   ├── recommendation_engine.py
│   ├── sentiment_analyzer.py
│   ├── weather_analyzer.py
│   └── translation_service.py
├── start_ai_service.bat  # Windows startup script
└── README.md            # This file
```

### Adding New AI Features

1. Create a new module in `ai_modules/`
2. Implement the required functionality
3. Add the module to `ai_modules/__init__.py`
4. Create a new endpoint in `app.py`
5. Update this README with usage examples

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the PORT in the .env file or kill the process using the port
2. **Missing dependencies**: Run `pip install -r requirements.txt`
3. **Python version**: Ensure you're using Python 3.8 or higher

### Logs

The service logs to the console. Check for error messages when starting the service.

## Future Enhancements

- Integration with real translation APIs (Google Translate, DeepL)
- Real weather API integration
- Machine learning models for better predictions
- Natural language processing for itinerary generation
- Real-time flight and hotel data integration 