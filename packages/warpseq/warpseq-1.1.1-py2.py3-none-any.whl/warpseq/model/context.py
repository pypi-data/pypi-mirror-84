class Context(object):

    # where am I?

    __slots__ = ('song', 'clip', 'track', 'pattern', 'scene', 'player', 'scene', 'scale', 'track', 'base_length')

    def __init__(self, song=None, clip=None, pattern=None, player=None, scene=None, scale=None, track=None, base_length=None):

        self.song = song
        self.clip = clip
        self.pattern = pattern

        self.scene = scene
        self.player = player
        self.track = track
        self.scene = scene
        self.scale = scale
        self.base_length = base_length


    def mark_playing(self, ts):

        # record the timestamp on all the objects so we can report on what is currently playing

        if self.scale:
            self.scale._played_ts = ts

        self.pattern._played_ts = ts


