import json
import random
from typing import Dict, List, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CostPredictor:
    def __init__(self):
        self.cost_data = self._load_cost_data()
        self.seasonal_factors = self._load_seasonal_factors()
        
    def _load_cost_data(self) -> Dict[str, Any]:
        """Load destination-specific cost data"""
        return {
            "Paris": {
                "accommodation": {"budget": 80, "mid": 150, "luxury": 400},
                "food": {"budget": 30, "mid": 60, "luxury": 120},
                "transportation": {"budget": 15, "mid": 25, "luxury": 50},
                "activities": {"budget": 20, "mid": 40, "luxury": 80},
                "cost_index": 1.2
            },
            "Tokyo": {
                "accommodation": {"budget": 70, "mid": 140, "luxury": 350},
                "food": {"budget": 25, "mid": 50, "luxury": 100},
                "transportation": {"budget": 12, "mid": 20, "luxury": 40},
                "activities": {"budget": 18, "mid": 35, "luxury": 70},
                "cost_index": 1.1
            },
            "New York": {
                "accommodation": {"budget": 100, "mid": 200, "luxury": 500},
                "food": {"budget": 35, "mid": 70, "luxury": 140},
                "transportation": {"budget": 20, "mid": 30, "luxury": 60},
                "activities": {"budget": 25, "mid": 50, "luxury": 100},
                "cost_index": 1.4
            }
        }
    
    def _load_seasonal_factors(self) -> Dict[str, float]:
        """Load seasonal cost multipliers"""
        return {
            "spring": 1.1,
            "summer": 1.3,
            "autumn": 1.0,
            "winter": 0.8
        }
    
    def predict(self, destination: str, duration: int, travel_style: str = "balanced",
               group_size: int = 1, season: str = None) -> Dict[str, Any]:
        """Predict travel costs for a destination"""
        
        # Get base cost data
        dest_costs = self.cost_data.get(destination, self._get_generic_costs(destination))
        
        # Determine cost tier based on travel style
        cost_tier = self._get_cost_tier(travel_style)
        
        # Calculate daily costs
        daily_costs = {
            "accommodation": dest_costs["accommodation"][cost_tier] * group_size,
            "food": dest_costs["food"][cost_tier] * group_size,
            "transportation": dest_costs["transportation"][cost_tier] * group_size,
            "activities": dest_costs["activities"][cost_tier] * group_size
        }
        
        # Apply seasonal factor
        seasonal_factor = self.seasonal_factors.get(season, 1.0) if season else 1.0
        
        # Calculate total costs
        total_daily = sum(daily_costs.values()) * seasonal_factor
        total_trip = total_daily * duration
        
        # Add miscellaneous costs
        misc_costs = total_trip * 0.1  # 10% for miscellaneous expenses
        
        return {
            "destination": destination,
            "duration": duration,
            "travelStyle": travel_style,
            "groupSize": group_size,
            "season": season,
            "dailyBreakdown": {
                "accommodation": round(daily_costs["accommodation"] * seasonal_factor, 2),
                "food": round(daily_costs["food"] * seasonal_factor, 2),
                "transportation": round(daily_costs["transportation"] * seasonal_factor, 2),
                "activities": round(daily_costs["activities"] * seasonal_factor, 2),
                "total": round(total_daily, 2)
            },
            "totalCost": round(total_trip + misc_costs, 2),
            "miscellaneous": round(misc_costs, 2),
            "seasonalFactor": seasonal_factor,
            "costIndex": dest_costs.get("cost_index", 1.0),
            "recommendations": self._generate_cost_recommendations(destination, travel_style, total_trip)
        }
    
    def _get_cost_tier(self, travel_style: str) -> str:
        """Map travel style to cost tier"""
        style_mapping = {
            "budget": "budget",
            "balanced": "mid",
            "luxury": "luxury",
            "adventure": "budget",
            "cultural": "mid",
            "relaxation": "luxury"
        }
        return style_mapping.get(travel_style, "mid")
    
    def _get_generic_costs(self, destination: str) -> Dict[str, Any]:
        """Generate generic cost data for unknown destinations"""
        return {
            "accommodation": {"budget": 60, "mid": 120, "luxury": 300},
            "food": {"budget": 25, "mid": 50, "luxury": 100},
            "transportation": {"budget": 15, "mid": 25, "luxury": 50},
            "activities": {"budget": 20, "mid": 40, "luxury": 80},
            "cost_index": 1.0
        }
    
    def _generate_cost_recommendations(self, destination: str, travel_style: str, total_cost: float) -> List[str]:
        """Generate cost-saving recommendations"""
        recommendations = []
        
        if travel_style == "budget":
            recommendations.extend([
                "Consider staying in hostels or budget accommodations",
                "Use public transportation instead of taxis",
                "Eat at local markets and street food vendors",
                "Look for free activities and attractions",
                "Book flights and accommodations in advance"
            ])
        elif travel_style == "luxury":
            recommendations.extend([
                "Book premium experiences and services",
                "Consider all-inclusive packages",
                "Opt for private transportation",
                "Reserve at high-end restaurants",
                "Include spa and wellness experiences"
            ])
        
        # Add general recommendations
        recommendations.extend([
            f"Research {destination} cost of living before your trip",
            "Set aside 10-15% of your budget for unexpected expenses",
            "Consider travel insurance for additional protection"
        ])
        
        return recommendations
    
    def optimize_budget(self, total_budget: float, destination: str, duration: int,
                       preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize budget allocation across different categories"""
        
        # Get base costs
        dest_costs = self.cost_data.get(destination, self._get_generic_costs(destination))
        
        # Calculate optimal allocation based on preferences
        allocation = {
            "accommodation": 0.4,  # 40% default
            "food": 0.25,          # 25% default
            "transportation": 0.15, # 15% default
            "activities": 0.15,    # 15% default
            "miscellaneous": 0.05  # 5% default
        }
        
        # Adjust based on preferences
        if preferences.get("food_focused"):
            allocation["food"] += 0.1
            allocation["accommodation"] -= 0.05
            allocation["activities"] -= 0.05
        
        if preferences.get("activity_focused"):
            allocation["activities"] += 0.1
            allocation["accommodation"] -= 0.05
            allocation["food"] -= 0.05
        
        if preferences.get("luxury_accommodation"):
            allocation["accommodation"] += 0.1
            allocation["food"] -= 0.05
            allocation["activities"] -= 0.05
        
        # Calculate daily budget
        daily_budget = total_budget / duration
        
        # Calculate category budgets
        category_budgets = {}
        for category, percentage in allocation.items():
            category_budgets[category] = round(daily_budget * percentage, 2)
        
        # Generate recommendations
        recommendations = self._generate_optimization_recommendations(
            destination, category_budgets, preferences
        )
        
        return {
            "totalBudget": total_budget,
            "dailyBudget": round(daily_budget, 2),
            "duration": duration,
            "destination": destination,
            "categoryAllocation": category_budgets,
            "recommendations": recommendations,
            "budgetEfficiency": self._calculate_budget_efficiency(category_budgets, dest_costs)
        }
    
    def _generate_optimization_recommendations(self, destination: str, 
                                            category_budgets: Dict[str, float],
                                            preferences: Dict[str, Any]) -> List[str]:
        """Generate budget optimization recommendations"""
        recommendations = []
        
        # Accommodation recommendations
        if category_budgets["accommodation"] < 50:
            recommendations.append("Consider hostels or shared accommodations")
        elif category_budgets["accommodation"] > 200:
            recommendations.append("Look for luxury hotels or resorts")
        
        # Food recommendations
        if category_budgets["food"] < 30:
            recommendations.append("Focus on street food and local markets")
        elif category_budgets["food"] > 80:
            recommendations.append("Consider fine dining experiences")
        
        # Activity recommendations
        if category_budgets["activities"] < 20:
            recommendations.append("Look for free activities and attractions")
        elif category_budgets["activities"] > 60:
            recommendations.append("Consider premium tours and experiences")
        
        return recommendations
    
    def _calculate_budget_efficiency(self, category_budgets: Dict[str, float],
                                   dest_costs: Dict[str, Any]) -> Dict[str, str]:
        """Calculate budget efficiency for each category"""
        efficiency = {}
        
        for category, budget in category_budgets.items():
            if category in dest_costs:
                avg_cost = sum(dest_costs[category].values()) / 3
                if budget < avg_cost * 0.8:
                    efficiency[category] = "budget"
                elif budget > avg_cost * 1.2:
                    efficiency[category] = "luxury"
                else:
                    efficiency[category] = "balanced"
        
        return efficiency 