from config import config


class Songinfo:
    """A wrapper for information about the song currently being played."""

    def __init__(self, uploader, creator, title, duration, like_count, dislike_count, webpage_url):
        self.uploader = uploader
        self.creator = creator
        self.title = title
        self.duration = duration
        self.like_count = like_count
        self.dislike_count = dislike_count
        self.webpage_url = webpage_url

        self._output = ""
        self.format_output()

    @property
    def output(self):
        return self._output

    def format_output(self):
        self._output = "```[" + self.title + "]\n"
        self._output += config.SONGINFO_UPLOADER + str(self.uploader) + "\n"
        self._output += config.SONGINFO_DURATION + str(self.duration) + config.SONGINFO_SECONDS + "\n"
        self._output += config.SONGINFO_LIKES + str(self.like_count) + "\n"
        self._output += config.SONGINFO_DISLIKES + str(self.dislike_count)
        self._output += "```\n" + str(self.webpage_url)
