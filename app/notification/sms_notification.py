from .notification_strategy import NotificationStrategy

class SMSNotificationStrategy(NotificationStrategy):
    
    def send_notification(self, message: str):
        print("Implement SMS notification")
