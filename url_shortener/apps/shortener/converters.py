

class UrlKeyConverter:
    regex = '[a-zA-Z0-9\-_]{4,7}'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return str(value)
