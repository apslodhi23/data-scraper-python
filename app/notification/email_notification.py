from .notification_strategy import NotificationStrategy

class EmailNotificationStrategy(NotificationStrategy):

    def send_notification(self, message: str):
        print("Implement Email notification")
