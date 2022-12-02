from dataclasses import dataclass, field


class Echo:

    def write(self, value):
        return value


@dataclass
class UrlFields:
    redirect_url: str = field(default='redirect_url')
    url_key: str = field(default='url_key')
    key: str = field(default='key')
    tag: str = field(default='tag')
    usage_count: str = field(default='usage_count')
