import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ItineraryGenerator:
    def __init__(self):
        self.destination_data = self._load_destination_data()
        self.activity_templates = self._load_activity_templates()
        
    def _load_destination_data(self) -> Dict[str, Any]:
        """Load destination-specific data and attractions"""
        return {
            "Paris": {
                "attractions": [
                    {"name": "Eiffel Tower", "type": "landmark", "duration": 2, "cost": 30},
                    {"name": "Louvre Museum", "type": "museum", "duration": 3, "cost": 20},
                    {"name": "Notre-Dame Cathedral", "type": "religious", "duration": 1, "cost": 0},
                    {"name": "Arc de Triomphe", "type": "landmark", "duration": 1, "cost": 15},
                    {"name": "Champs-Élysées", "type": "shopping", "duration": 2, "cost": 0},
                    {"name": "Montmartre", "type": "cultural", "duration": 2, "cost": 0},
                    {"name": "Seine River Cruise", "type": "activity", "duration": 1, "cost": 25}
                ],
                "restaurants": ["Le Jules Verne", "L'Astrance", "Le Comptoir du Relais"],
                "hotels": ["Hotel Ritz Paris", "Le Bristol", "Hotel Plaza Athenee"],
                "transportation": ["Metro", "Bus", "Walking", "Taxi"]
            },
            "Tokyo": {
                "attractions": [
                    {"name": "Senso-ji Temple", "type": "religious", "duration": 2, "cost": 0},
                    {"name": "Tokyo Skytree", "type": "landmark", "duration": 2, "cost": 25},
                    {"name": "Shibuya Crossing", "type": "cultural", "duration": 1, "cost": 0},
                    {"name": "Tsukiji Fish Market", "type": "food", "duration": 2, "cost": 0},
                    {"name": "Meiji Shrine", "type": "religious", "duration": 1, "cost": 0},
                    {"name": "Tokyo Disneyland", "type": "entertainment", "duration": 8, "cost": 80}
                ],
                "restaurants": ["Sukiyabashi Jiro", "Narisawa", "Den"],
                "hotels": ["Park Hyatt Tokyo", "Aman Tokyo", "Mandarin Oriental"],
                "transportation": ["JR Rail", "Metro", "Walking", "Taxi"]
            },
            "New York": {
                "attractions": [
                    {"name": "Statue of Liberty", "type": "landmark", "duration": 3, "cost": 25},
                    {"name": "Central Park", "type": "nature", "duration": 2, "cost": 0},
                    {"name": "Times Square", "type": "cultural", "duration": 1, "cost": 0},
                    {"name": "Metropolitan Museum", "type": "museum", "duration": 3, "cost": 25},
                    {"name": "Empire State Building", "type": "landmark", "duration": 2, "cost": 40},
                    {"name": "Broadway Show", "type": "entertainment", "duration": 3, "cost": 150}
                ],
                "restaurants": ["Le Bernardin", "Eleven Madison Park", "Per Se"],
                "hotels": ["The Plaza", "Waldorf Astoria", "The Ritz-Carlton"],
                "transportation": ["Subway", "Bus", "Walking", "Taxi"]
            }
        }
    
    def _load_activity_templates(self) -> Dict[str, List[str]]:
        """Load activity templates for different travel styles"""
        return {
            "budget": [
                "Free walking tour of {destination}",
                "Visit local markets and street food",
                "Explore public parks and gardens",
                "Attend free cultural events",
                "Use public transportation",
                "Stay in hostels or budget hotels"
            ],
            "luxury": [
                "Private guided tour of {destination}",
                "Fine dining at Michelin-starred restaurants",
                "Luxury spa and wellness experiences",
                "Private transportation and chauffeur",
                "Exclusive access to attractions",
                "Stay in 5-star hotels and resorts"
            ],
            "adventure": [
                "Hiking and outdoor activities",
                "Water sports and adventure tours",
                "Rock climbing and extreme sports",
                "Camping and wilderness experiences",
                "Off-road and 4x4 adventures",
                "Wildlife and nature photography"
            ],
            "cultural": [
                "Museum and gallery visits",
                "Historical site exploration",
                "Local cooking classes",
                "Traditional craft workshops",
                "Cultural performance attendance",
                "Language and cultural immersion"
            ],
            "relaxation": [
                "Spa and wellness retreats",
                "Beach and coastal relaxation",
                "Meditation and yoga sessions",
                "Hot springs and thermal baths",
                "Peaceful nature walks",
                "Quiet countryside stays"
            ]
        }
    
    def generate(self, destination: str, start_date: str, end_date: str, 
                budget: float, travel_style: str = "balanced", 
                interests: List[str] = None, group_size: int = 1) -> Dict[str, Any]:
        """Generate a complete travel itinerary"""
        
        # Parse dates
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        duration = (end_dt - start_dt).days + 1
        
        # Get destination data
        dest_data = self.destination_data.get(destination, self._get_generic_destination_data(destination))
        
        # Generate daily itinerary
        days = []
        total_cost = 0
        
        for day_num in range(1, duration + 1):
            current_date = start_dt + timedelta(days=day_num - 1)
            
            # Generate day activities
            day_activities = self._generate_day_activities(
                destination, dest_data, travel_style, interests, budget, day_num
            )
            
            # Calculate day cost
            day_cost = sum(activity.get('cost', 0) for activity in day_activities)
            total_cost += day_cost
            
            days.append({
                "dayNumber": day_num,
                "date": current_date.strftime("%Y-%m-%d"),
                "activities": day_activities,
                "accommodation": self._generate_accommodation(destination, travel_style, budget),
                "transportation": self._generate_transportation(destination, travel_style),
                "estimatedCost": day_cost
            })
        
        # Generate travel tips
        travel_tips = self.generate_travel_tips(destination, travel_style, interests or [])
        
        return {
            "title": f"{destination} Adventure",
            "destination": destination,
            "startDate": start_date,
            "endDate": end_date,
            "duration": duration,
            "travelStyle": travel_style,
            "budget": budget,
            "estimatedTotalCost": total_cost,
            "days": days,
            "travelTips": travel_tips,
            "recommendations": self._generate_recommendations(destination, travel_style, interests)
        }
    
    def _generate_day_activities(self, destination: str, dest_data: Dict, 
                               travel_style: str, interests: List[str], 
                               budget: float, day_num: int) -> List[Dict]:
        """Generate activities for a specific day"""
        activities = []
        available_attractions = dest_data.get("attractions", [])
        
        # Filter attractions based on interests and travel style
        filtered_attractions = self._filter_attractions(available_attractions, interests, travel_style)
        
        # Select activities for the day
        selected_attractions = random.sample(
            filtered_attractions, 
            min(3, len(filtered_attractions))
        )
        
        current_time = 9  # Start at 9 AM
        
        for i, attraction in enumerate(selected_attractions):
            activity = {
                "time": f"{current_time:02d}:00",
                "activity": attraction["name"],
                "location": destination,
                "description": f"Visit {attraction['name']} - {attraction['type']} experience",
                "estimatedCost": attraction["cost"],
                "duration": attraction["duration"],
                "type": attraction["type"],
                "bookingStatus": "pending"
            }
            
            activities.append(activity)
            current_time += attraction["duration"] + 1  # Add 1 hour for travel between activities
            
            # Add lunch break
            if i == 1:  # After second activity
                activities.append({
                    "time": f"{current_time:02d}:00",
                    "activity": "Lunch Break",
                    "location": destination,
                    "description": "Enjoy local cuisine",
                    "estimatedCost": 15 if travel_style == "budget" else 50,
                    "duration": 1,
                    "type": "food",
                    "bookingStatus": "pending"
                })
                current_time += 1
        
        return activities
    
    def _filter_attractions(self, attractions: List[Dict], interests: List[str], 
                          travel_style: str) -> List[Dict]:
        """Filter attractions based on interests and travel style"""
        if not interests:
            return attractions
        
        filtered = []
        for attraction in attractions:
            # Check if attraction type matches interests
            if any(interest.lower() in attraction["type"].lower() for interest in interests):
                filtered.append(attraction)
        
        return filtered if filtered else attractions
    
    def _generate_accommodation(self, destination: str, travel_style: str, budget: float) -> Dict:
        """Generate accommodation recommendation"""
        accommodation_types = {
            "budget": {"type": "hostel", "cost": 30, "description": "Budget-friendly hostel"},
            "luxury": {"type": "5-star hotel", "cost": 300, "description": "Luxury 5-star hotel"},
            "adventure": {"type": "camping", "cost": 20, "description": "Adventure camping"},
            "cultural": {"type": "boutique hotel", "cost": 150, "description": "Cultural boutique hotel"},
            "relaxation": {"type": "resort", "cost": 250, "description": "Relaxing resort"}
        }
        
        acc_type = accommodation_types.get(travel_style, accommodation_types["budget"])
        
        return {
            "name": f"{destination} {acc_type['type'].title()}",
            "location": destination,
            "cost": acc_type["cost"],
            "type": acc_type["type"],
            "description": acc_type["description"],
            "bookingStatus": "pending"
        }
    
    def _generate_transportation(self, destination: str, travel_style: str) -> List[Dict]:
        """Generate transportation recommendations"""
        transport_options = {
            "budget": ["public transport", "walking"],
            "luxury": ["private car", "taxi"],
            "adventure": ["bicycle", "hiking"],
            "cultural": ["public transport", "walking"],
            "relaxation": ["private car", "walking"]
        }
        
        options = transport_options.get(travel_style, ["public transport", "walking"])
        
        return [
            {
                "type": option,
                "from": "Hotel",
                "to": "City Center",
                "departureTime": "09:00",
                "arrivalTime": "09:30",
                "cost": 5 if option == "public transport" else 20,
                "bookingStatus": "pending"
            }
            for option in options[:2]  # Limit to 2 options
        ]
    
    def _get_generic_destination_data(self, destination: str) -> Dict:
        """Generate generic data for unknown destinations"""
        return {
            "attractions": [
                {"name": f"{destination} City Center", "type": "cultural", "duration": 2, "cost": 0},
                {"name": f"{destination} Museum", "type": "museum", "duration": 2, "cost": 15},
                {"name": f"{destination} Park", "type": "nature", "duration": 1, "cost": 0},
                {"name": f"{destination} Market", "type": "food", "duration": 1, "cost": 0}
            ],
            "restaurants": [f"Local {destination} Restaurant"],
            "hotels": [f"{destination} Hotel"],
            "transportation": ["Public Transport", "Walking", "Taxi"]
        }
    
    def _generate_recommendations(self, destination: str, travel_style: str, 
                                interests: List[str]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Add travel style specific recommendations
        if travel_style in self.activity_templates:
            for template in self.activity_templates[travel_style][:3]:
                recommendations.append(template.format(destination=destination))
        
        # Add interest-based recommendations
        if interests:
            for interest in interests:
                if "food" in interest.lower():
                    recommendations.append(f"Try local {destination} cuisine")
                elif "culture" in interest.lower():
                    recommendations.append(f"Visit {destination} cultural sites")
                elif "nature" in interest.lower():
                    recommendations.append(f"Explore {destination} natural attractions")
        
        return recommendations
    
    def generate_travel_tips(self, destination: str, travel_style: str = None, 
                           interests: List[str] = None, experience_level: str = "intermediate") -> List[str]:
        """Generate personalized travel tips"""
        tips = []
        
        # General tips
        tips.extend([
            f"Research local customs and etiquette in {destination}",
            "Pack appropriate clothing for the destination's climate",
            "Keep important documents and emergency contacts handy",
            "Learn basic phrases in the local language",
            "Have travel insurance for unexpected situations"
        ])
        
        # Style-specific tips
        if travel_style == "budget":
            tips.extend([
                "Use public transportation to save money",
                "Eat at local markets and street food vendors",
                "Book accommodations in advance for better rates",
                "Look for free activities and attractions"
            ])
        elif travel_style == "luxury":
            tips.extend([
                "Book premium services and experiences in advance",
                "Consider hiring a local guide for personalized experiences",
                "Reserve at high-end restaurants early",
                "Opt for premium transportation options"
            ])
        
        # Experience level tips
        if experience_level == "beginner":
            tips.extend([
                "Start with popular tourist destinations",
                "Join guided tours for better understanding",
                "Stay in well-reviewed accommodations",
                "Plan your itinerary in detail"
            ])
        elif experience_level == "expert":
            tips.extend([
                "Explore off-the-beaten-path locations",
                "Connect with locals for authentic experiences",
                "Be flexible with your plans",
                "Try unique local experiences"
            ])
        
        return tips[:10]  # Limit to 10 tips 