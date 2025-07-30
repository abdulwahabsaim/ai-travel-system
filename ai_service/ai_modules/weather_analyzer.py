import json
import random
from typing import Dict, List, Any
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class WeatherAnalyzer:
    def __init__(self):
        self.weather_data = self._load_weather_data()
        self.seasonal_patterns = self._load_seasonal_patterns()
        
    def _load_weather_data(self) -> Dict[str, Any]:
        """Load destination-specific weather data"""
        return {
            "Paris": {
                "climate": "temperate",
                "seasons": {
                    "spring": {"temp_range": (8, 18), "rainfall": "moderate", "sunshine": "good"},
                    "summer": {"temp_range": (15, 25), "rainfall": "low", "sunshine": "excellent"},
                    "autumn": {"temp_range": (10, 20), "rainfall": "moderate", "sunshine": "good"},
                    "winter": {"temp_range": (2, 8), "rainfall": "high", "sunshine": "low"}
                },
                "best_months": [5, 6, 9, 10],
                "rainy_months": [11, 12, 1, 2],
                "peak_season": [6, 7, 8]
            },
            "Tokyo": {
                "climate": "temperate",
                "seasons": {
                    "spring": {"temp_range": (10, 20), "rainfall": "moderate", "sunshine": "good"},
                    "summer": {"temp_range": (20, 30), "rainfall": "high", "sunshine": "moderate"},
                    "autumn": {"temp_range": (15, 25), "rainfall": "moderate", "sunshine": "good"},
                    "winter": {"temp_range": (0, 10), "rainfall": "low", "sunshine": "good"}
                },
                "best_months": [3, 4, 10, 11],
                "rainy_months": [6, 7, 8, 9],
                "peak_season": [3, 4, 10, 11]
            },
            "Bali": {
                "climate": "tropical",
                "seasons": {
                    "dry": {"temp_range": (25, 35), "rainfall": "low", "sunshine": "excellent"},
                    "wet": {"temp_range": (23, 32), "rainfall": "high", "sunshine": "moderate"}
                },
                "best_months": [4, 5, 6, 7, 8, 9],
                "rainy_months": [10, 11, 12, 1, 2, 3],
                "peak_season": [6, 7, 8]
            },
            "New York": {
                "climate": "temperate",
                "seasons": {
                    "spring": {"temp_range": (5, 18), "rainfall": "moderate", "sunshine": "good"},
                    "summer": {"temp_range": (18, 30), "rainfall": "moderate", "sunshine": "excellent"},
                    "autumn": {"temp_range": (8, 20), "rainfall": "moderate", "sunshine": "good"},
                    "winter": {"temp_range": (-5, 5), "rainfall": "moderate", "sunshine": "low"}
                },
                "best_months": [4, 5, 9, 10],
                "rainy_months": [3, 4, 5, 6, 7, 8, 9, 10, 11],
                "peak_season": [6, 7, 8]
            }
        }
    
    def _load_seasonal_patterns(self) -> Dict[str, List[str]]:
        """Load seasonal weather patterns and recommendations"""
        return {
            "spring": [
                "Mild temperatures perfect for outdoor activities",
                "Cherry blossoms in many destinations",
                "Good time for sightseeing and cultural activities",
                "Pack layers for variable weather"
            ],
            "summer": [
                "Warm weather ideal for beach and outdoor activities",
                "Peak tourist season with higher prices",
                "Longer daylight hours for exploration",
                "Pack light clothing and sun protection"
            ],
            "autumn": [
                "Comfortable temperatures for travel",
                "Beautiful fall colors in many destinations",
                "Fewer crowds than summer",
                "Pack layers for cooler evenings"
            ],
            "winter": [
                "Cold weather, pack warm clothing",
                "Lower prices and fewer crowds",
                "Winter sports and activities available",
                "Shorter daylight hours"
            ],
            "dry": [
                "Excellent weather for outdoor activities",
                "Minimal rainfall, pack light",
                "Good time for beach and adventure activities",
                "Stay hydrated in hot temperatures"
            ],
            "wet": [
                "Rainy season, pack rain gear",
                "Lush landscapes and fewer crowds",
                "Indoor activities recommended",
                "Lower prices during off-peak season"
            ]
        }
    
    def get_insights(self, destination: str, travel_dates: Dict[str, str]) -> Dict[str, Any]:
        """Get weather insights for travel planning"""
        
        # Get destination weather data
        dest_weather = self.weather_data.get(destination, self._get_generic_weather_data(destination))
        
        # Parse travel dates
        start_date = datetime.strptime(travel_dates["start"], "%Y-%m-%d")
        end_date = datetime.strptime(travel_dates["end"], "%Y-%m-%d")
        
        # Determine season and weather conditions
        season = self._determine_season(start_date, dest_weather["climate"])
        weather_conditions = dest_weather["seasons"].get(season, {})
        
        # Calculate trip duration
        duration = (end_date - start_date).days + 1
        
        # Generate weather forecast (simulated)
        weather_forecast = self._generate_weather_forecast(destination, start_date, duration, weather_conditions)
        
        # Analyze weather suitability
        suitability_analysis = self._analyze_weather_suitability(destination, season, weather_conditions, duration)
        
        # Generate packing recommendations
        packing_recommendations = self._generate_packing_recommendations(season, weather_conditions, duration)
        
        # Generate activity recommendations
        activity_recommendations = self._generate_activity_recommendations(season, weather_conditions)
        
        return {
            "destination": destination,
            "travelDates": travel_dates,
            "duration": duration,
            "season": season,
            "weatherConditions": weather_conditions,
            "weatherForecast": weather_forecast,
            "suitabilityAnalysis": suitability_analysis,
            "packingRecommendations": packing_recommendations,
            "activityRecommendations": activity_recommendations,
            "bestTimeToVisit": self._determine_best_time_to_visit(destination),
            "weatherAlerts": self._generate_weather_alerts(weather_conditions, season)
        }
    
    def _determine_season(self, date: datetime, climate: str) -> str:
        """Determine season based on date and climate"""
        month = date.month
        
        if climate == "tropical":
            if month in [4, 5, 6, 7, 8, 9]:
                return "dry"
            else:
                return "wet"
        else:  # temperate climate
            if month in [3, 4, 5]:
                return "spring"
            elif month in [6, 7, 8]:
                return "summer"
            elif month in [9, 10, 11]:
                return "autumn"
            else:
                return "winter"
    
    def _generate_weather_forecast(self, destination: str, start_date: datetime, 
                                 duration: int, weather_conditions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate weather forecast for the trip duration"""
        forecast = []
        
        for day in range(duration):
            current_date = start_date + timedelta(days=day)
            
            # Simulate weather based on conditions
            temp_range = weather_conditions.get("temp_range", (15, 25))
            avg_temp = (temp_range[0] + temp_range[1]) / 2
            temp_variation = random.uniform(-3, 3)
            daily_temp = round(avg_temp + temp_variation, 1)
            
            # Determine weather conditions
            rainfall_chance = self._calculate_rainfall_chance(weather_conditions.get("rainfall", "moderate"))
            sunshine_hours = self._calculate_sunshine_hours(weather_conditions.get("sunshine", "good"))
            
            forecast.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "dayOfWeek": current_date.strftime("%A"),
                "temperature": {
                    "high": round(daily_temp + 3, 1),
                    "low": round(daily_temp - 3, 1),
                    "average": daily_temp
                },
                "conditions": {
                    "rainfall": rainfall_chance,
                    "sunshine": sunshine_hours,
                    "description": self._get_weather_description(daily_temp, rainfall_chance)
                }
            })
        
        return forecast
    
    def _calculate_rainfall_chance(self, rainfall_level: str) -> float:
        """Calculate rainfall probability based on level"""
        rainfall_chances = {
            "low": 0.1,
            "moderate": 0.3,
            "high": 0.6
        }
        return rainfall_chances.get(rainfall_level, 0.3)
    
    def _calculate_sunshine_hours(self, sunshine_level: str) -> int:
        """Calculate sunshine hours based on level"""
        sunshine_hours = {
            "low": 4,
            "moderate": 6,
            "good": 8,
            "excellent": 10
        }
        return sunshine_hours.get(sunshine_level, 6)
    
    def _get_weather_description(self, temperature: float, rainfall_chance: float) -> str:
        """Get weather description based on temperature and rainfall"""
        if rainfall_chance > 0.5:
            return "Rainy"
        elif temperature > 25:
            return "Hot and sunny"
        elif temperature > 15:
            return "Mild and pleasant"
        elif temperature > 5:
            return "Cool"
        else:
            return "Cold"
    
    def _analyze_weather_suitability(self, destination: str, season: str, 
                                   weather_conditions: Dict[str, Any], duration: int) -> Dict[str, Any]:
        """Analyze weather suitability for travel"""
        
        temp_range = weather_conditions.get("temp_range", (15, 25))
        avg_temp = (temp_range[0] + temp_range[1]) / 2
        rainfall = weather_conditions.get("rainfall", "moderate")
        sunshine = weather_conditions.get("sunshine", "good")
        
        # Calculate suitability scores
        temperature_score = self._calculate_temperature_score(avg_temp)
        rainfall_score = self._calculate_rainfall_score(rainfall)
        sunshine_score = self._calculate_sunshine_score(sunshine)
        
        overall_score = (temperature_score + rainfall_score + sunshine_score) / 3
        
        return {
            "overallScore": round(overall_score, 2),
            "temperatureScore": round(temperature_score, 2),
            "rainfallScore": round(rainfall_score, 2),
            "sunshineScore": round(sunshine_score, 2),
            "suitability": self._get_suitability_level(overall_score),
            "recommendations": self._get_suitability_recommendations(overall_score, season)
        }
    
    def _calculate_temperature_score(self, temperature: float) -> float:
        """Calculate temperature suitability score (0-1)"""
        if 15 <= temperature <= 25:
            return 1.0
        elif 10 <= temperature <= 30:
            return 0.8
        elif 5 <= temperature <= 35:
            return 0.6
        else:
            return 0.3
    
    def _calculate_rainfall_score(self, rainfall: str) -> float:
        """Calculate rainfall suitability score (0-1)"""
        rainfall_scores = {
            "low": 1.0,
            "moderate": 0.7,
            "high": 0.4
        }
        return rainfall_scores.get(rainfall, 0.7)
    
    def _calculate_sunshine_score(self, sunshine: str) -> float:
        """Calculate sunshine suitability score (0-1)"""
        sunshine_scores = {
            "low": 0.4,
            "moderate": 0.7,
            "good": 0.9,
            "excellent": 1.0
        }
        return sunshine_scores.get(sunshine, 0.7)
    
    def _get_suitability_level(self, score: float) -> str:
        """Get suitability level based on score"""
        if score >= 0.8:
            return "excellent"
        elif score >= 0.6:
            return "good"
        elif score >= 0.4:
            return "fair"
        else:
            return "poor"
    
    def _get_suitability_recommendations(self, score: float, season: str) -> List[str]:
        """Get recommendations based on suitability score"""
        recommendations = []
        
        if score >= 0.8:
            recommendations.append("Excellent weather conditions for travel")
            recommendations.append("Perfect time to visit this destination")
        elif score >= 0.6:
            recommendations.append("Good weather conditions overall")
            recommendations.append("Consider packing for variable weather")
        elif score >= 0.4:
            recommendations.append("Weather conditions are acceptable")
            recommendations.append("Be prepared for some weather challenges")
        else:
            recommendations.append("Weather conditions may impact your trip")
            recommendations.append("Consider alternative dates or indoor activities")
        
        # Add seasonal recommendations
        if season in self.seasonal_patterns:
            recommendations.extend(self.seasonal_patterns[season])
        
        return recommendations
    
    def _generate_packing_recommendations(self, season: str, weather_conditions: Dict[str, Any], 
                                        duration: int) -> Dict[str, List[str]]:
        """Generate packing recommendations based on weather"""
        
        temp_range = weather_conditions.get("temp_range", (15, 25))
        rainfall = weather_conditions.get("rainfall", "moderate")
        
        clothing = []
        accessories = []
        essentials = []
        
        # Clothing recommendations
        if temp_range[1] > 25:
            clothing.extend(["Light cotton clothing", "Shorts and t-shirts", "Summer dresses"])
        elif temp_range[0] < 10:
            clothing.extend(["Warm jacket", "Thermal underwear", "Winter boots"])
        else:
            clothing.extend(["Light layers", "Sweaters", "Comfortable walking shoes"])
        
        # Accessory recommendations
        if rainfall == "high":
            accessories.extend(["Waterproof jacket", "Umbrella", "Waterproof shoes"])
        if temp_range[1] > 25:
            accessories.extend(["Sunglasses", "Sun hat", "Sunscreen"])
        if temp_range[0] < 10:
            accessories.extend(["Gloves", "Scarf", "Warm hat"])
        
        # Essential items
        essentials.extend([
            "Travel documents",
            "First aid kit",
            "Phone charger",
            "Camera"
        ])
        
        if duration > 7:
            essentials.append("Laundry supplies")
        
        return {
            "clothing": clothing,
            "accessories": accessories,
            "essentials": essentials
        }
    
    def _generate_activity_recommendations(self, season: str, weather_conditions: Dict[str, Any]) -> List[str]:
        """Generate activity recommendations based on weather"""
        
        temp_range = weather_conditions.get("temp_range", (15, 25))
        rainfall = weather_conditions.get("rainfall", "moderate")
        sunshine = weather_conditions.get("sunshine", "good")
        
        activities = []
        
        # Temperature-based activities
        if temp_range[1] > 25:
            activities.extend([
                "Beach activities",
                "Swimming",
                "Outdoor dining",
                "Sunset viewing"
            ])
        elif temp_range[0] < 10:
            activities.extend([
                "Indoor museums",
                "Hot springs",
                "Winter sports",
                "Cozy cafes"
            ])
        else:
            activities.extend([
                "Walking tours",
                "Outdoor sightseeing",
                "Hiking",
                "Photography"
            ])
        
        # Rainfall-based activities
        if rainfall == "high":
            activities.extend([
                "Indoor attractions",
                "Shopping malls",
                "Museums and galleries",
                "Spa and wellness"
            ])
        
        # Sunshine-based activities
        if sunshine in ["good", "excellent"]:
            activities.extend([
                "Outdoor photography",
                "Picnics",
                "Outdoor markets",
                "Park visits"
            ])
        
        return activities
    
    def _determine_best_time_to_visit(self, destination: str) -> Dict[str, Any]:
        """Determine the best time to visit a destination"""
        dest_weather = self.weather_data.get(destination, self._get_generic_weather_data(destination))
        
        best_months = dest_weather.get("best_months", [4, 5, 6, 9, 10])
        peak_season = dest_weather.get("peak_season", [6, 7, 8])
        
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        
        return {
            "bestMonths": [month_names[month-1] for month in best_months],
            "peakSeason": [month_names[month-1] for month in peak_season],
            "reasoning": f"Best weather conditions and fewer crowds during {', '.join([month_names[month-1] for month in best_months])}"
        }
    
    def _generate_weather_alerts(self, weather_conditions: Dict[str, Any], season: str) -> List[str]:
        """Generate weather alerts and warnings"""
        alerts = []
        
        temp_range = weather_conditions.get("temp_range", (15, 25))
        rainfall = weather_conditions.get("rainfall", "moderate")
        
        if temp_range[1] > 30:
            alerts.append("High temperature alert - stay hydrated and avoid midday sun")
        
        if temp_range[0] < 0:
            alerts.append("Freezing temperatures - pack warm clothing")
        
        if rainfall == "high":
            alerts.append("Heavy rainfall expected - pack rain gear and plan indoor activities")
        
        if season == "summer":
            alerts.append("Peak season - expect higher prices and crowds")
        
        return alerts
    
    def _get_generic_weather_data(self, destination: str) -> Dict[str, Any]:
        """Generate generic weather data for unknown destinations"""
        return {
            "climate": "temperate",
            "seasons": {
                "spring": {"temp_range": (10, 20), "rainfall": "moderate", "sunshine": "good"},
                "summer": {"temp_range": (18, 28), "rainfall": "moderate", "sunshine": "excellent"},
                "autumn": {"temp_range": (8, 18), "rainfall": "moderate", "sunshine": "good"},
                "winter": {"temp_range": (0, 10), "rainfall": "moderate", "sunshine": "low"}
            },
            "best_months": [4, 5, 6, 9, 10],
            "rainy_months": [11, 12, 1, 2],
            "peak_season": [6, 7, 8]
        } 