from .notification_strategy import NotificationStrategy

class ConsoleNotificationStrategy(NotificationStrategy):
    def send_notification(self, message: str):
        print(message)
