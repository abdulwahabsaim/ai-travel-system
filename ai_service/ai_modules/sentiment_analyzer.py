import re
from typing import Dict, Any, List
import logging
from textblob import TextBlob

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        self.positive_words = self._load_positive_words()
        self.negative_words = self._load_negative_words()
        self.travel_keywords = self._load_travel_keywords()
        
    def _load_positive_words(self) -> List[str]:
        """Load positive sentiment words"""
        return [
            "amazing", "wonderful", "excellent", "fantastic", "great", "good", "nice",
            "beautiful", "stunning", "breathtaking", "incredible", "perfect", "lovely",
            "enjoyable", "pleasant", "satisfying", "outstanding", "superb", "brilliant",
            "fabulous", "terrific", "awesome", "magnificent", "gorgeous", "charming",
            "delightful", "memorable", "unforgettable", "spectacular", "impressive"
        ]
    
    def _load_negative_words(self) -> List[str]:
        """Load negative sentiment words"""
        return [
            "terrible", "awful", "horrible", "bad", "poor", "disappointing", "frustrating",
            "annoying", "boring", "dull", "mediocre", "average", "overpriced", "expensive",
            "crowded", "noisy", "dirty", "uncomfortable", "stressful", "difficult",
            "problematic", "unpleasant", "unsatisfactory", "inadequate", "inferior",
            "subpar", "lousy", "miserable", "depressing", "disgusting"
        ]
    
    def _load_travel_keywords(self) -> Dict[str, List[str]]:
        """Load travel-specific keywords for analysis"""
        return {
            "accommodation": ["hotel", "room", "bed", "clean", "comfortable", "noisy", "small"],
            "food": ["restaurant", "meal", "delicious", "tasty", "fresh", "expensive", "cheap"],
            "service": ["staff", "friendly", "helpful", "rude", "slow", "efficient", "professional"],
            "location": ["central", "convenient", "accessible", "remote", "far", "close", "walking"],
            "value": ["worth", "price", "expensive", "cheap", "reasonable", "overpriced", "bargain"],
            "atmosphere": ["ambiance", "vibe", "mood", "relaxing", "busy", "quiet", "lively"]
        }
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of travel-related text"""
        
        # Clean and preprocess text
        cleaned_text = self._preprocess_text(text)
        
        # Perform sentiment analysis
        sentiment_scores = self._calculate_sentiment_scores(cleaned_text)
        
        # Extract travel-specific insights
        travel_insights = self._extract_travel_insights(cleaned_text)
        
        # Determine overall sentiment
        overall_sentiment = self._determine_overall_sentiment(sentiment_scores)
        
        # Generate recommendations
        recommendations = self._generate_sentiment_recommendations(sentiment_scores, travel_insights)
        
        return {
            "text": text,
            "cleanedText": cleaned_text,
            "overallSentiment": overall_sentiment,
            "sentimentScores": sentiment_scores,
            "travelInsights": travel_insights,
            "recommendations": recommendations,
            "confidence": self._calculate_confidence(sentiment_scores)
        }
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _calculate_sentiment_scores(self, text: str) -> Dict[str, float]:
        """Calculate various sentiment scores"""
        words = text.split()
        
        # Count positive and negative words
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        
        # Calculate ratios
        total_words = len(words)
        positive_ratio = positive_count / total_words if total_words > 0 else 0
        negative_ratio = negative_count / total_words if total_words > 0 else 0
        
        # Use TextBlob for additional sentiment analysis
        blob = TextBlob(text)
        textblob_polarity = blob.sentiment.polarity
        textblob_subjectivity = blob.sentiment.subjectivity
        
        # Calculate custom sentiment score
        custom_score = (positive_ratio - negative_ratio) * 2  # Scale to -1 to 1
        
        return {
            "positiveRatio": round(positive_ratio, 3),
            "negativeRatio": round(negative_ratio, 3),
            "textblobPolarity": round(textblob_polarity, 3),
            "textblobSubjectivity": round(textblob_subjectivity, 3),
            "customScore": round(custom_score, 3),
            "positiveWords": positive_count,
            "negativeWords": negative_count,
            "totalWords": total_words
        }
    
    def _extract_travel_insights(self, text: str) -> Dict[str, Any]:
        """Extract travel-specific insights from text"""
        insights = {}
        words = text.split()
        
        for category, keywords in self.travel_keywords.items():
            category_words = [word for word in words if word in keywords]
            if category_words:
                insights[category] = {
                    "keywords": category_words,
                    "count": len(category_words),
                    "sentiment": self._analyze_category_sentiment(category_words)
                }
        
        # Extract common travel phrases
        travel_phrases = self._extract_travel_phrases(text)
        if travel_phrases:
            insights["phrases"] = travel_phrases
        
        return insights
    
    def _analyze_category_sentiment(self, words: List[str]) -> str:
        """Analyze sentiment for a specific category of words"""
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _extract_travel_phrases(self, text: str) -> List[str]:
        """Extract common travel-related phrases"""
        phrases = []
        
        # Common travel phrases
        travel_phrases = [
            "great location", "excellent service", "amazing experience",
            "worth the money", "highly recommend", "would visit again",
            "poor service", "not worth it", "disappointing experience",
            "great value", "overpriced", "clean and comfortable"
        ]
        
        for phrase in travel_phrases:
            if phrase in text:
                phrases.append(phrase)
        
        return phrases
    
    def _determine_overall_sentiment(self, sentiment_scores: Dict[str, float]) -> str:
        """Determine overall sentiment based on multiple scores"""
        # Weight different scores
        custom_weight = 0.4
        textblob_weight = 0.4
        ratio_weight = 0.2
        
        # Calculate weighted score
        weighted_score = (
            sentiment_scores["customScore"] * custom_weight +
            sentiment_scores["textblobPolarity"] * textblob_weight +
            (sentiment_scores["positiveRatio"] - sentiment_scores["negativeRatio"]) * ratio_weight
        )
        
        # Determine sentiment category
        if weighted_score > 0.1:
            return "positive"
        elif weighted_score < -0.1:
            return "negative"
        else:
            return "neutral"
    
    def _calculate_confidence(self, sentiment_scores: Dict[str, float]) -> float:
        """Calculate confidence in the sentiment analysis"""
        # Higher confidence with more words and stronger signals
        word_confidence = min(sentiment_scores["totalWords"] / 50, 1.0)  # Cap at 50 words
        
        # Confidence based on sentiment strength
        sentiment_strength = abs(sentiment_scores["textblobPolarity"])
        
        # Combine factors
        confidence = (word_confidence + sentiment_strength) / 2
        
        return round(confidence, 3)
    
    def _generate_sentiment_recommendations(self, sentiment_scores: Dict[str, float],
                                          travel_insights: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on sentiment analysis"""
        recommendations = []
        
        overall_sentiment = self._determine_overall_sentiment(sentiment_scores)
        
        if overall_sentiment == "positive":
            recommendations.extend([
                "This review indicates a positive experience",
                "Consider this destination for similar travelers",
                "The positive feedback suggests good value for money"
            ])
        elif overall_sentiment == "negative":
            recommendations.extend([
                "This review indicates areas for improvement",
                "Consider addressing the mentioned concerns",
                "May want to look for alternative options"
            ])
        else:
            recommendations.extend([
                "This review shows mixed feelings",
                "Consider additional reviews for better perspective",
                "The experience seems average overall"
            ])
        
        # Add category-specific recommendations
        for category, insight in travel_insights.items():
            if category != "phrases":
                if insight["sentiment"] == "negative":
                    recommendations.append(f"Consider improving {category} based on feedback")
                elif insight["sentiment"] == "positive":
                    recommendations.append(f"{category.title()} received positive feedback")
        
        return recommendations
    
    def analyze_multiple_reviews(self, reviews: List[str]) -> Dict[str, Any]:
        """Analyze multiple reviews and provide aggregate insights"""
        if not reviews:
            return {"error": "No reviews provided"}
        
        # Analyze each review
        individual_analyses = [self.analyze(review) for review in reviews]
        
        # Calculate aggregate statistics
        sentiments = [analysis["overallSentiment"] for analysis in individual_analyses]
        positive_count = sentiments.count("positive")
        negative_count = sentiments.count("negative")
        neutral_count = sentiments.count("neutral")
        
        # Calculate average scores
        avg_polarity = sum(analysis["sentimentScores"]["textblobPolarity"] for analysis in individual_analyses) / len(reviews)
        avg_subjectivity = sum(analysis["sentimentScores"]["textblobSubjectivity"] for analysis in individual_analyses) / len(reviews)
        
        # Determine overall sentiment
        if positive_count > negative_count:
            overall_sentiment = "positive"
        elif negative_count > positive_count:
            overall_sentiment = "negative"
        else:
            overall_sentiment = "neutral"
        
        return {
            "totalReviews": len(reviews),
            "overallSentiment": overall_sentiment,
            "sentimentDistribution": {
                "positive": positive_count,
                "negative": negative_count,
                "neutral": neutral_count
            },
            "averageScores": {
                "polarity": round(avg_polarity, 3),
                "subjectivity": round(avg_subjectivity, 3)
            },
            "individualAnalyses": individual_analyses,
            "summary": f"Overall {overall_sentiment} sentiment with {positive_count} positive, {negative_count} negative, and {neutral_count} neutral reviews"
        } 