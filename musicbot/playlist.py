from collections import deque


class Playlist:
    MAX_HISTORY_LENGTH = 10

    def __init__(self):
        self.playque = deque()
        self.playhistory = deque()

    def add(self, track):
        self.playque.append(track)

    def next(self):
        self.playhistory.append(self.playque.popleft())

        if len(self.playque) == 0:
            return None
        return self.playque[0]

    def prev(self):
        if len(self.playhistory) == 0:
            dummy = "DummySong"
            self.playque.appendleft(dummy)
            return dummy
        self.playque.appendleft(self.playhistory.pop())
        return self.playque[0]

    def empty(self):
        self.playque.clear()
        self.playhistory.clear()
