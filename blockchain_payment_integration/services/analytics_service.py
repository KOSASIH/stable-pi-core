import logging
import requests

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self, analytics_api_url):
        self.analytics_api_url = analytics_api_url

    def track_event(self, event_name, properties):
        """Track an event with the analytics service."""
        payload = {
            "event": event_name,
            "properties": properties
        }
        try:
            response = requests.post(self.analytics_api_url, json=payload)
            response.raise_for_status()
            logger.info("Event tracked successfully: %s", event_name)
        except requests.exceptions.HTTPError as http_err:
            logger.error("HTTP error occurred while tracking event: %s", http_err)
        except Exception as err:
            logger.error("An error occurred while tracking event: %s", err)

    def track_payment_event(self, payment_id, user_id, status):
        """Track payment-related events."""
        properties = {
            "payment_id": payment_id,
            "user_id": user_id,
            "status": status
        }
        self.track_event("Payment Status Update", properties)
