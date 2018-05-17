from collections import deque

from config import config


class Playlist:
    """Stores the youtube links of songs to be played and already played and offers basic operation on the queues"""

    def __init__(self):
        # Stores the ytlinks os the songs in queue and the ones already played
        self.playque = deque()
        self.playhistory = deque()

        # A seperate history that remembers the names of the tracks that were played
        self.trackname_history = deque()

    def __len__(self):
        return len(self.playque)

    def add_name(self, trackname):
        self.trackname_history.append(trackname)
        if len(self.trackname_history) > config.MAX_TRACKNAME_HISTORY_LENGTH:
                self.trackname_history.popleft()

    def add(self, track):
        self.playque.append(track)

    def next(self):
        song_played = self.playque.popleft()
        if song_played != "Dummy":
            self.playhistory.append(song_played)
            if len(self.playhistory) > config.MAX_HISTORY_LENGTH:
                self.playhistory.popleft()
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
