# AI Travel System

A comprehensive travel planning and booking management system with advanced AI-powered features.

## 🚀 Features

### Core Features
- **User Authentication**: Secure registration and login system
- **Itinerary Management**: Create, edit, and manage travel itineraries
- **Booking Management**: Track flights, hotels, activities, and transportation
- **Dashboard**: Overview of trips, bookings, and travel statistics

### 🤖 AI-Powered Features
- **Intelligent Itinerary Generation**: AI creates personalized travel plans
- **Cost Prediction**: Advanced cost estimation with seasonal factors
- **Destination Recommendations**: Personalized suggestions based on preferences
- **Sentiment Analysis**: Analyze travel reviews and feedback
- **Weather Insights**: Weather-based travel planning and recommendations
- **Translation Service**: Multi-language support for international travel
- **Budget Optimization**: AI-powered budget allocation and optimization
- **Travel Tips**: Personalized travel advice and recommendations

## 🛠️ Technology Stack

### Backend Services
- **Node.js Application**: Express.js server with EJS templating
- **Python AI Service**: Flask-based AI service with multiple AI modules
- **Database**: MongoDB with Mongoose ODM
- **Authentication**: Session-based with bcrypt password hashing

### AI Modules (Python)
- **Itinerary Generator**: Creates personalized travel itineraries
- **Cost Predictor**: Predicts travel costs with seasonal analysis
- **Recommendation Engine**: Provides destination recommendations
- **Sentiment Analyzer**: Analyzes travel reviews and feedback
- **Weather Analyzer**: Weather insights and seasonal recommendations
- **Translation Service**: Multi-language translation and phrase guides

### Frontend
- **Templating**: EJS with responsive design
- **Styling**: Custom CSS with modern UI/UX
- **JavaScript**: Client-side interactions and API calls

## 📦 Installation

### Prerequisites
- Node.js (v14 or higher)
- Python (v3.8 or higher)
- MongoDB
- npm and pip package managers

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-travel-system
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Install Python AI service dependencies**
   ```bash
   cd ai_service
   pip install -r requirements.txt
   cd ..
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Start MongoDB**
   Make sure MongoDB is running on your system

6. **Seed the database (optional)**
   ```bash
   npm run seed
   ```

## 🚀 Running the Application

### Option 1: Start Both Services Together
```bash
start_both_services.bat
```

### Option 2: Start Services Separately

**Start Python AI Service:**
```bash
cd ai_service
python app.py
```

**Start Node.js Application:**
```bash
npm start
# or for development
npm run dev
```

### Service URLs
- **Node.js Application**: http://localhost:5000
- **Python AI Service**: http://localhost:5001

## 📚 Usage

### Basic Usage
1. **Register/Login**: Create an account or login with existing credentials
2. **Create Itineraries**: Plan your trips with destinations, dates, and activities
3. **Manage Bookings**: Track your travel bookings and expenses
4. **Use AI Assistant**: Get intelligent recommendations for your trips

### AI Features Usage
1. **Generate Itineraries**: Use AI to create complete travel plans
2. **Predict Costs**: Get accurate cost estimates for your trips
3. **Get Recommendations**: Receive personalized destination suggestions
4. **Analyze Reviews**: Understand sentiment in travel reviews
5. **Weather Planning**: Get weather insights for travel planning
6. **Translate**: Use translation services for international travel
7. **Optimize Budget**: Get AI-powered budget allocation advice

## 🔌 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/logout` - User logout

### Itineraries
- `GET /itinerary` - List user itineraries
- `POST /itinerary/create` - Create new itinerary
- `GET /itinerary/:id` - View itinerary details
- `POST /itinerary/:id/edit` - Edit itinerary
- `POST /itinerary/:id/delete` - Delete itinerary

### Bookings
- `GET /booking` - List user bookings
- `POST /booking/create` - Create new booking
- `GET /booking/:id` - View booking details
- `POST /booking/:id/edit` - Edit booking
- `POST /booking/:id/delete` - Delete booking

### AI Assistant (Node.js Routes)
- `POST /ai/generate-itinerary` - Generate AI-powered itinerary
- `POST /ai/predict-costs` - Get cost predictions
- `POST /ai/get-recommendations` - Get destination recommendations
- `POST /ai/analyze-sentiment` - Analyze sentiment of reviews
- `POST /ai/get-weather-insights` - Get weather insights
- `POST /ai/translate` - Translate text
- `POST /ai/optimize-budget` - Optimize budget allocation
- `POST /ai/generate-travel-tips` - Generate travel tips
- `GET /ai/health` - AI service health check

### AI Service (Python Direct Endpoints)
- `GET /health` - Service health status
- `POST /generate-itinerary` - Generate travel itinerary
- `POST /predict-costs` - Predict travel costs
- `POST /get-recommendations` - Get recommendations
- `POST /analyze-sentiment` - Analyze sentiment
- `POST /get-weather-insights` - Get weather insights
- `POST /translate` - Translate text
- `POST /optimize-budget` - Optimize budget
- `POST /generate-travel-tips` - Generate travel tips

## 🗄️ Database Schema

### User
- username, email, password (hashed)
- firstName, lastName
- preferences (travel style, budget, destinations)

### Itinerary
- user (reference), title, destination
- startDate, endDate, budget
- travelStyle, days (array of daily activities)
- status, notes

### Booking
- user (reference), itinerary (reference)
- bookingType (flight, hotel, activity, transportation)
- provider details, pricing, status
- bookingReference, confirmationNumber

## 🤖 AI Service Architecture

### Python AI Modules
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
└── README.md            # AI service documentation
```

### Integration
- Node.js application communicates with Python AI service via HTTP
- RESTful API endpoints for all AI features
- Error handling and fallback mechanisms
- Health checks for service monitoring

## 🧪 Testing

### Test Credentials (after seeding)
- **Email**: moiz@gmail.com, **Password**: moiz123
- **Email**: ali@gmail.com, **Password**: ali123

### Sample Data
The seed script creates:
- 2 users with different travel preferences
- 3 sample itineraries (European Adventure, Caribbean Paradise, Tokyo Exploration)
- 4 sample bookings (flight, hotel, activity, transportation)

## 🔧 Configuration

### Environment Variables
```env
# MongoDB Connection
MONGODB_URI=mongodb://localhost:27017/ai-travel-app

# Session Secret
SESSION_SECRET=your-super-secret-session-key

# Server Configuration
PORT=5000

# AI Service Configuration
AI_SERVICE_URL=http://localhost:5001
```

## 🚀 Deployment

### Production Setup
1. Set up production MongoDB instance
2. Configure environment variables for production
3. Set up reverse proxy (nginx) for both services
4. Use PM2 or similar for process management
5. Set up SSL certificates for HTTPS

### Docker Deployment (Future)
- Docker containers for both Node.js and Python services
- Docker Compose for orchestration
- MongoDB container for database

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly (both Node.js and Python services)
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:
1. Check the documentation in `ai_service/README.md`
2. Review the health check endpoint: `GET /ai/health`
3. Check service logs for error messages
4. Ensure both services are running on correct ports

## 🔮 Future Enhancements

- **Real-time Notifications**: WebSocket integration
- **External API Integration**: Weather, currency, flight APIs
- **Mobile App**: React Native companion app
- **Advanced AI**: Machine learning for better predictions
- **Social Features**: Share itineraries and travel tips
- **Payment Integration**: Stripe/PayPal for bookings
- **Multi-language Support**: Internationalization
- **Advanced Analytics**: Travel insights and reports

---

**Built with ❤️ using Node.js, Express, Python, Flask, MongoDB, and modern AI technologies.** 