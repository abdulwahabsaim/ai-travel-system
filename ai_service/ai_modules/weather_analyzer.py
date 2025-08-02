import requests
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class WeatherAnalyzer:
    GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

    def _get_coordinates(self, destination: str):
        """Get latitude and longitude for a destination."""
        params = {'name': destination, 'count': 1, 'language': 'en', 'format': 'json'}
        try:
            response = requests.get(self.GEOCODING_API_URL, params=params)
            response.raise_for_status()
            results = response.json().get('results')
            if results:
                return {
                    "latitude": results[0]["latitude"],
                    "longitude": results[0]["longitude"],
                    "timezone": results[0]["timezone"],
                    "country": results[0].get("country", "")
                }
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching coordinates for {destination}: {e}")
        return None

    def _get_weather_forecast_data(self, lat, lon, timezone):
        """Get 7-day weather forecast from Open-Meteo."""
        params = {
            'latitude': lat,
            'longitude': lon,
            'daily': 'weathercode,temperature_2m_max,temperature_2m_min',
            'timezone': timezone
        }
        try:
            response = requests.get(self.WEATHER_API_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather forecast: {e}")
        return None
        
    def _interpret_weather_code(self, code):
        """Convert WMO weather code to a human-readable string."""
        codes = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Depositing rime fog",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            56: "Light freezing drizzle", 57: "Dense freezing drizzle",
            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            66: "Light freezing rain", 67: "Heavy freezing rain",
            71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
            85: "Slight snow showers", 86: "Heavy snow showers",
            95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
        }
        return codes.get(code, "Unknown weather")

    def get_insights(self, destination: str, travel_dates: dict):
        """Get REAL weather insights for travel planning."""
        
        coords = self._get_coordinates(destination)
        if not coords:
            return {"error": f"Could not find location: {destination}"}

        weather_data = self._get_weather_forecast_data(coords['latitude'], coords['longitude'], coords['timezone'])
        if not weather_data:
            return {"error": "Could not retrieve weather data."}

        # Format the forecast
        daily_data = weather_data.get('daily', {})
        forecast = []
        for i, date_str in enumerate(daily_data.get('time', [])):
            forecast.append({
                "date": date_str,
                "dayOfWeek": datetime.strptime(date_str, "%Y-%m-%d").strftime("%A"),
                "temperature": {
                    "high": daily_data['temperature_2m_max'][i],
                    "low": daily_data['temperature_2m_min'][i]
                },
                "conditions": {
                    "description": self._interpret_weather_code(daily_data['weathercode'][i]),
                    "weather_code": daily_data['weathercode'][i]
                }
            })

        # Generate insights from the first day of the forecast as an example
        today_forecast = forecast[0]
        avg_temp = (today_forecast['temperature']['high'] + today_forecast['temperature']['low']) / 2

        return {
            "destination": destination,
            "country": coords.get('country'),
            "travelDates": travel_dates,
            "weatherForecast": forecast,
            "packingRecommendations": self._generate_packing_recommendations(today_forecast),
            "activityRecommendations": self._generate_activity_recommendations(today_forecast),
            "summary": f"The forecast for {destination} shows an average temperature around {avg_temp:.0f}°C with {today_forecast['conditions']['description'].lower()}."
        }

    def _generate_packing_recommendations(self, day_forecast):
        """Generate packing list based on a day's forecast."""
        high_temp = day_forecast['temperature']['high']
        weather_code = day_forecast['conditions']['weather_code']
        clothing, accessories = [], []

        if high_temp > 25:
            clothing.extend(["Shorts", "T-shirts", "Sandals"])
            accessories.append("Sunscreen and sunglasses")
        elif high_temp > 15:
            clothing.extend(["Jeans or trousers", "Light jacket or sweater"])
        else:
            clothing.extend(["Warm jacket", "Sweaters", "Long pants"])
        
        if weather_code >= 51: # Drizzle, Rain, or Showers
            accessories.append("Umbrella or waterproof jacket")
        if weather_code >= 71: # Snow
             accessories.extend(["Gloves", "Scarf", "Warm hat"])

        return {"clothing": clothing, "accessories": accessories, "essentials": ["Travel documents", "Chargers", "Medication"]}

    def _generate_activity_recommendations(self, day_forecast):
        """Generate activity ideas based on weather."""
        high_temp = day_forecast['temperature']['high']
        weather_code = day_forecast['conditions']['weather_code']
        
        if weather_code in [0, 1, 2]: # Clear or partly cloudy
            if high_temp > 18:
                return ["Walking tour", "Picnic in a park", "Outdoor sightseeing"]
            else:
                return ["Visit outdoor markets", "Explore the city on foot"]
        elif weather_code >= 51: # Rain or worse
            return ["Visit museums and art galleries", "Go shopping", "Enjoy a cozy cafe"]
        else:
            return ["Explore local neighborhoods", "Visit indoor attractions"]