import difflib


class IntentRouter:
    def __init__(self):
        self.routes = {}

    def register(self, keyword, module):
        self.routes[keyword] = module

    def dispatch(self, text):
        text_lower = text.lower()

        for keyword in self.routes:
            if keyword in text_lower:
                return keyword, self.routes[keyword]

        words = text_lower.split()

        for word in words:
            close = difflib.get_close_matches(
                word, self.routes.keys(), n=1, cutoff=0.75
            )
            if close:
                return close[0], self.routes[close[0]]

        return None, None
