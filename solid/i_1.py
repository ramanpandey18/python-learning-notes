
from abc import ABC, abstractmethod


class EmailSender(ABC):
    @abstractmethod
    def send_email(self, message):
        pass


class SMSSender(ABC):
    @abstractmethod
    def send_sms(self, message):
        pass


class PushSender(ABC):
    @abstractmethod
    def send_push(self, message):
        pass


class EmailNotifier(EmailSender):
    def send_email(self, message):
        print(f"Sending email: {message}")


class SMSNotifier(SMSSender):
    def send_sms(self, message):
        print(f"Sending SMS: {message}")


class MultiChannelNotifier(EmailSender, SMSSender):
    def send_email(self, message):
        print(f"Sending email: {message}")

    def send_sms(self, message):
        print(f"Sending SMS: {message}")
