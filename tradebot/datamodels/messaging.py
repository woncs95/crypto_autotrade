from dataclasses import dataclass

@dataclass
class TelegramMessage:
    recipient: str
    content: str