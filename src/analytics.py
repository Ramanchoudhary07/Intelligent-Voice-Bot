"""
Analytics module for tracking bot performance
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from config import settings
import logging

logger = logging.getLogger(__name__)


class Analytics:
    """Handles analytics and performance tracking"""
    
    def __init__(self):
        """Initialize analytics"""
        self.enabled = settings.analytics_enabled
        self.data_file = settings.analytics_dir / "analytics.json"
        self.metrics = {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "average_response_time": 0,
            "intent_distribution": {},
            "error_rates": {},
            "queries_by_hour": {}
        }
        self._load_metrics()
    
    def _load_metrics(self):
        """Load metrics from file"""
        if self.data_file.exists():
            try:
                with open(self.data_file, "r") as f:
                    self.metrics = json.load(f)
            except Exception as e:
                logger.error(f"Error loading analytics: {str(e)}")
    
    def _save_metrics(self):
        """Save metrics to file"""
        if not self.enabled:
            return
        
        try:
            with open(self.data_file, "w") as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving analytics: {str(e)}")
    
    def track_query(
        self,
        query_text: str,
        intent: str,
        response_time: int,
        success: bool,
        error: str = None
    ):
        """
        Track a query
        
        Args:
            query_text: User query text
            intent: Detected intent
            response_time: Response time in milliseconds
            success: Whether the query was successful
            error: Error message if any
        """
        if not self.enabled:
            return
        
        self.metrics["total_queries"] += 1
        
        if success:
            self.metrics["successful_queries"] += 1
        else:
            self.metrics["failed_queries"] += 1
            if error:
                self.metrics["error_rates"][error] = self.metrics["error_rates"].get(error, 0) + 1
        
        # Update average response time
        total = self.metrics["total_queries"]
        current_avg = self.metrics["average_response_time"]
        self.metrics["average_response_time"] = (
            (current_avg * (total - 1) + response_time) / total
        )
        
        # Track intent distribution
        self.metrics["intent_distribution"][intent] = (
            self.metrics["intent_distribution"].get(intent, 0) + 1
        )
        
        # Track queries by hour
        hour = datetime.now().hour
        self.metrics["queries_by_hour"][str(hour)] = (
            self.metrics["queries_by_hour"].get(str(hour), 0) + 1
        )
        
        self._save_metrics()
    
    def get_metrics(self) -> Dict:
        """
        Get current metrics
        
        Returns:
            Dictionary of metrics
        """
        return self.metrics.copy()
    
    def get_summary(self) -> Dict:
        """
        Get analytics summary
        
        Returns:
            Summary dictionary
        """
        total = self.metrics["total_queries"]
        if total == 0:
            return {"message": "No data available"}
        
        success_rate = (self.metrics["successful_queries"] / total) * 100
        failure_rate = (self.metrics["failed_queries"] / total) * 100
        
        return {
            "total_queries": total,
            "successful_queries": self.metrics["successful_queries"],
            "failed_queries": self.metrics["failed_queries"],
            "success_rate": f"{success_rate:.2f}%",
            "failure_rate": f"{failure_rate:.2f}%",
            "average_response_time_ms": f"{self.metrics['average_response_time']:.2f}",
            "intent_distribution": self.metrics["intent_distribution"],
            "error_rates": self.metrics["error_rates"]
        }

