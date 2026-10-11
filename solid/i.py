
from abc import ABC, abstractmethod


class NotificationService(ABC):
    @abstractmethod
    def send_email(self, message):
        pass

    @abstractmethod
    def send_sms(self, message):
        pass

    @abstractmethod
    def send_push(self, message):
        pass


class EmailNotifier(NotificationService):
    def send_email(self, message):
        print(f"Sending email: {message}")

    def send_sms(self, message):
        raise NotImplementedError

    def send_push(self, message):
        raise NotImplementedError
