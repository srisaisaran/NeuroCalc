from intent_router import IntentRouter


class NeuroCalcCore:

    def __init__(self):
        self.router = IntentRouter()

    def process(self, message):
        return self.router.process(message)