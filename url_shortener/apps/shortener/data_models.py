from dataclasses import dataclass, field
from datetime import datetime
from typing import Union


@dataclass
class UrlRowErrorMessage:
    redirect_url: str = None
    key: str = None
    tag: str = None
    expired: str = None


@dataclass
class UrlRow:
    redirect_url: str
    tag: str
    key: str = field(default=None)
    expired: Union[str, datetime] = field(default=None)
    message: UrlRowErrorMessage = None

    def __post_init__(self):
        if self.redirect_url:
            self.redirect_url = self.redirect_url.strip()
        if self.key:
            self.key = str(self.key).strip()
        if self.tag:
            self.tag = str(self.tag).strip()
        if self.expired and isinstance(self.expired, str):
            self.expired = datetime.strptime(self.expired, '%Y-%m-%d')

    def is_valid(self) -> bool:
        valid = bool(self.redirect_url and self.tag)
        if valid:
            return valid

        self.message = UrlRowErrorMessage()
        if not self.redirect_url:
            self.message.redirect_url = '`redirect_url` აუცილებელია'
        if not self.tag:
            self.message.tag = '`tag` აუცილებელია'

        return False
