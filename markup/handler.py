from typing import List


class Handler:
    '''hello'''

    def callback(self, prefix: str, name: str, *args: List[str]):
        method = getattr(self, prefix+name, None)
        if callable(method):
            return method(*args)

    def start(self, name: str):
        self.callback('start_', name)

    def end(self, name: str):
        self.callback('end_', name)

    def sub(self, name: str):
        def substituion(match):
            result = self.callback("sub_", name, match)
            if result is None:
                match.group(0)
            return result
        return substituion
