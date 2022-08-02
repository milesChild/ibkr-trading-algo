import time


class textView:
    description = None

    def __init__(self):
        self.description = "Basic Text Viewing Class"

    def renderMessage(self, str):
        print(str)

    def renderMessageAndPause(self, str):
        self.renderMessage(str)
        time.sleep(.5)