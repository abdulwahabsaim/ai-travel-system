import json
import random
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class RecommendationEngine:
    def __init__(self):
        self.destination_database = self._load_destination_database()
        self.user_preference_weights = self._load_preference_weights()
        
    def _load_destination_database(self) -> Dict[str, Any]:
        """Load comprehensive destination database"""
        return {
            "destinations": {
                "Paris": {
                    "category": "city",
                    "region": "Europe",
                    "climate": "temperate",
                    "cost_level": "high",
                    "best_seasons": ["spring", "autumn"],
                    "activities": ["culture", "food", "romance", "shopping"],
                    "travel_styles": ["luxury", "cultural", "romantic"],
                    "rating": 4.8,
                    "popularity": 0.95
                },
                "Tokyo": {
                    "category": "city",
                    "region": "Asia",
                    "climate": "temperate",
                    "cost_level": "high",
                    "best_seasons": ["spring", "autumn"],
                    "activities": ["culture", "food", "technology", "shopping"],
                    "travel_styles": ["cultural", "adventure", "luxury"],
                    "rating": 4.7,
                    "popularity": 0.92
                },
                "Bali": {
                    "category": "island",
                    "region": "Asia",
                    "climate": "tropical",
                    "cost_level": "medium",
                    "best_seasons": ["dry"],
                    "activities": ["beach", "relaxation", "culture", "adventure"],
                    "travel_styles": ["relaxation", "adventure", "budget"],
                    "rating": 4.6,
                    "popularity": 0.88
                },
                "New York": {
                    "category": "city",
                    "region": "North America",
                    "climate": "temperate",
                    "cost_level": "high",
                    "best_seasons": ["spring", "autumn"],
                    "activities": ["culture", "food", "shopping", "entertainment"],
                    "travel_styles": ["luxury", "cultural", "adventure"],
                    "rating": 4.5,
                    "popularity": 0.90
                },
                "Santorini": {
                    "category": "island",
                    "region": "Europe",
                    "climate": "mediterranean",
                    "cost_level": "high",
                    "best_seasons": ["spring", "autumn"],
                    "activities": ["romance", "relaxation", "culture", "beach"],
                    "travel_styles": ["luxury", "romantic", "relaxation"],
                    "rating": 4.9,
                    "popularity": 0.94
                }
            }
        }
    
    def _load_preference_weights(self) -> Dict[str, float]:
        """Load weights for different preference factors"""
        return {
            "cost_level": 0.25,
            "activities": 0.30,
            "travel_style": 0.20,
            "climate": 0.15,
            "popularity": 0.10
        }
    
    def get_recommendations(self, user_preferences: Dict[str, Any], 
                          budget_range: Dict[str, float] = None,
                          travel_history: List[str] = None,
                          interests: List[str] = None) -> Dict[str, Any]:
        """Get personalized travel recommendations"""
        
        # Calculate destination scores
        destination_scores = self._calculate_destination_scores(
            user_preferences, budget_range, travel_history, interests
        )
        
        # Sort destinations by score
        sorted_destinations = sorted(
            destination_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Get top recommendations
        top_recommendations = []
        for destination, score in sorted_destinations[:5]:
            dest_data = self.destination_database["destinations"][destination]
            recommendation = {
                "destination": destination,
                "score": round(score, 3),
                "category": dest_data["category"],
                "region": dest_data["region"],
                "cost_level": dest_data["cost_level"],
                "best_seasons": dest_data["best_seasons"],
                "activities": dest_data["activities"],
                "travel_styles": dest_data["travel_styles"],
                "rating": dest_data["rating"],
                "popularity": dest_data["popularity"],
                "reasoning": self._generate_recommendation_reasoning(
                    destination, user_preferences, interests
                )
            }
            top_recommendations.append(recommendation)
        
        # Generate alternative recommendations
        alternative_recommendations = self._generate_alternative_recommendations(
            user_preferences, budget_range, interests
        )
        
        return {
            "topRecommendations": top_recommendations,
            "alternativeRecommendations": alternative_recommendations,
            "userPreferences": user_preferences,
            "budgetRange": budget_range,
            "interests": interests,
            "travelHistory": travel_history
        }
    
    def _calculate_destination_scores(self, user_preferences: Dict[str, Any],
                                    budget_range: Dict[str, float],
                                    travel_history: List[str],
                                    interests: List[str]) -> Dict[str, float]:
        """Calculate scores for each destination based on user preferences"""
        scores = {}
        
        for destination, dest_data in self.destination_database["destinations"].items():
            score = 0.0
            
            # Skip if already visited
            if travel_history and destination in travel_history:
                continue
            
            # Cost level matching
            if budget_range and "cost_level" in user_preferences:
                cost_match = self._calculate_cost_match(
                    dest_data["cost_level"], 
                    user_preferences["cost_level"],
                    budget_range
                )
                score += cost_match * self.user_preference_weights["cost_level"]
            
            # Activities matching
            if interests:
                activity_match = self._calculate_activity_match(
                    dest_data["activities"], interests
                )
                score += activity_match * self.user_preference_weights["activities"]
            
            # Travel style matching
            if "travel_style" in user_preferences:
                style_match = self._calculate_style_match(
                    dest_data["travel_styles"], 
                    user_preferences["travel_style"]
                )
                score += style_match * self.user_preference_weights["travel_style"]
            
            # Climate matching
            if "climate_preference" in user_preferences:
                climate_match = self._calculate_climate_match(
                    dest_data["climate"], 
                    user_preferences["climate_preference"]
                )
                score += climate_match * self.user_preference_weights["climate"]
            
            # Popularity and rating
            popularity_score = dest_data["popularity"] * self.user_preference_weights["popularity"]
            score += popularity_score
            
            scores[destination] = score
        
        return scores
    
    def _calculate_cost_match(self, dest_cost_level: str, user_cost_level: str,
                            budget_range: Dict[str, float]) -> float:
        """Calculate cost level matching score"""
        cost_mapping = {"low": 1, "medium": 2, "high": 3}
        
        dest_cost = cost_mapping.get(dest_cost_level, 2)
        user_cost = cost_mapping.get(user_cost_level, 2)
        
        # Perfect match
        if dest_cost == user_cost:
            return 1.0
        
        # Adjacent levels
        if abs(dest_cost - user_cost) == 1:
            return 0.7
        
        # Far levels
        return 0.3
    
    def _calculate_activity_match(self, dest_activities: List[str], 
                                user_interests: List[str]) -> float:
        """Calculate activity matching score"""
        if not user_interests:
            return 0.5
        
        matches = 0
        for interest in user_interests:
            if any(interest.lower() in activity.lower() for activity in dest_activities):
                matches += 1
        
        return matches / len(user_interests)
    
    def _calculate_style_match(self, dest_styles: List[str], user_style: str) -> float:
        """Calculate travel style matching score"""
        if user_style in dest_styles:
            return 1.0
        elif any(style in dest_styles for style in ["balanced", "mixed"]):
            return 0.7
        else:
            return 0.3
    
    def _calculate_climate_match(self, dest_climate: str, user_climate: str) -> float:
        """Calculate climate matching score"""
        if dest_climate == user_climate:
            return 1.0
        elif user_climate == "any":
            return 0.8
        else:
            return 0.4
    
    def _generate_recommendation_reasoning(self, destination: str,
                                         user_preferences: Dict[str, Any],
                                         interests: List[str]) -> str:
        """Generate reasoning for why a destination was recommended"""
        dest_data = self.destination_database["destinations"][destination]
        reasons = []
        
        # Cost reasoning
        if "cost_level" in user_preferences:
            if dest_data["cost_level"] == user_preferences["cost_level"]:
                reasons.append(f"Matches your {dest_data['cost_level']} budget preference")
        
        # Activity reasoning
        if interests:
            matching_activities = [
                activity for activity in dest_data["activities"]
                if any(interest.lower() in activity.lower() for interest in interests)
            ]
            if matching_activities:
                reasons.append(f"Perfect for {', '.join(matching_activities)} activities")
        
        # Travel style reasoning
        if "travel_style" in user_preferences:
            if user_preferences["travel_style"] in dest_data["travel_styles"]:
                reasons.append(f"Ideal for {user_preferences['travel_style']} travel")
        
        # Rating reasoning
        if dest_data["rating"] >= 4.5:
            reasons.append("Highly rated by travelers")
        
        return "; ".join(reasons) if reasons else "Great overall destination"
    
    def _generate_alternative_recommendations(self, user_preferences: Dict[str, Any],
                                            budget_range: Dict[str, float],
                                            interests: List[str]) -> List[Dict[str, Any]]:
        """Generate alternative recommendations based on different criteria"""
        alternatives = []
        
        # Budget alternatives
        if budget_range and budget_range.get("max") < 2000:
            alternatives.append({
                "type": "budget_friendly",
                "destinations": ["Bali", "Thailand", "Vietnam", "Portugal", "Greece"],
                "reasoning": "Great value for money destinations"
            })
        
        # Adventure alternatives
        if interests and any("adventure" in interest.lower() for interest in interests):
            alternatives.append({
                "type": "adventure",
                "destinations": ["New Zealand", "Iceland", "Costa Rica", "Nepal", "Peru"],
                "reasoning": "Perfect for adventure seekers"
            })
        
        # Cultural alternatives
        if interests and any("culture" in interest.lower() for interest in interests):
            alternatives.append({
                "type": "cultural",
                "destinations": ["Italy", "Spain", "Japan", "India", "Morocco"],
                "reasoning": "Rich cultural experiences"
            })
        
        # Relaxation alternatives
        if user_preferences.get("travel_style") == "relaxation":
            alternatives.append({
                "type": "relaxation",
                "destinations": ["Maldives", "Seychelles", "Bora Bora", "Maui", "Fiji"],
                "reasoning": "Perfect for relaxation and wellness"
            })
        
        return alternatives 