# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

# this class contains play-head logic to support processing events
# into MIDI notes. This class isn't meant to be used directly,
# use Multiplayer as shown in api/public.py instead.

# FAIR WARNING: this code has some larger functions because it is trying to be more efficient

from ..api.callbacks import Callbacks
from ..api.exceptions import *
from ..model.event import NOTE_OFF, Event
import time

NOTE_GAP = .001

def event_sorter(evt):
    return evt.time

class Player(object):

    __slots__ = [ 'clip', 'song', 'engine', 'left_to_play', 'time_index', 'repeat_count', 'clip_length_in_ms', 'events', '_multiplayer', 'callbacks', 'stopped' ]


    def __init__(self, clip=None, song=None, engine=None):
        """
        When we start a player we ask clips for all the events between a start
        time and a hypothetical start time. The player class can then walk through
        them in steps.
        """

        self.clip = clip
        self.song = song
        self.engine = engine
        self.time_index = 0
        self.left_to_play = None
        self.clip_length_in_ms = self.clip.get_clip_duration(self.song)
        self.events = self.clip.get_events(self.song)
        self.repeat_count = self.clip.repeat
        self.callbacks = Callbacks()
        self.stopped = False
        self.start()

    def get_multiplayer(self):
        return self._multiplayer

    def wait_time(self):
        return min([ x.time for x in self.left_to_play ]) - self.time_index

    def has_events(self):
        if len(self.left_to_play):
            return True
        return False

    def due(self):
        return [x for x in self.left_to_play if x.time <= self.time_index]

    def empty(self):
        return len(self.left_to_play) == 0

    def inject_off_event(self, event):

        note = event.note
        self.left_to_play.append(Event(
            type = NOTE_OFF,
            on_event = event,
            time = event.time + note.length - NOTE_GAP,
            note = note.copy(),
            song = event.song,
            track = event.track,
            clip = event.clip,
            player = self,
            from_context = event.from_context
        ))

    def _still_on_this_clip(self):
        """
        We are due to still be playing this clip if the clip has infinite repeats
        or the repeats are expired.
        """
        if self.clip.repeat is None or self.clip.repeat == 0:
            # infinite repeats
            return True
        self.repeat_count = self.repeat_count - 1
        if self.repeat_count <= 0:
            return False
        return True

    def advance(self, milliseconds, now):
        """
        Advances the playhead a number of milliseconds and plays all the notes
        between those two points.
        """

        t1 = time.perf_counter()

        self.clip._played_ts = now
        self.clip.scene._played_ts = now

        self.time_index += milliseconds

        ltp = self.left_to_play

        # consume any events we need to off the time queue
        if (not self.stopped) and len(self.left_to_play):

            due = self.due()

            if len(due):
                due = sorted(due, key=event_sorter)
                for x in due:

                    x.song = self.song
                    x.clip = self.clip
                    x.track = self.clip.track
                    x.player = self

                    self.engine.play(x, now)
                self.left_to_play = [ x for x in ltp if x not in due ]

        if self.stopped or self.time_index >= self.clip_length_in_ms:

            # the play-head has advanced beyond the end of the clip

            if (not self.stopped) and self._still_on_this_clip():
                # the clip is due to repeat again...
                self.callbacks.on_clip_restart(self.clip)
                # recompute events so randomness can change
                self.events = self.clip.get_events(self.song)
                self.start()
            else:
                # the clip isn't due to repeat again, make sure we have played any note off events
                # before removing it

                self.stop()

                if self.clip.auto_scene_advance:

                    print("the clip is set to auto advance the scene")

                    # see if the clip says to go play a new scene
                    new_scene = self.song.next_scene(self.clip.scene)
                    if new_scene:
                        self._multiplayer.remove_clip(self.clip, add_pending=True)

                        new_clips = new_scene.clips(self.song)
                        if (len(new_clips) == 0) and self._multiplayer.stop_if_empty:
                            self._multiplayer.stop()

                        self._multiplayer.add_scene(new_scene)

                        #t2 = time.perf_counter()
                        #print("ADVANCE1: %s" % (t2-t1))

                        return

                else:
                    pass

                if self.clip.next_clip is not None:


                    new_clip = self.song.find_clip_by_name(self.clip.next_clip)

                    self._multiplayer.remove_clip(self.clip, add_pending=True)
                    self._multiplayer.add_clips([new_clip])

                    #t2 = time.perf_counter()
                    #print("ADVANCE2: %s" % (t2 - t1))

                    return

                self._multiplayer.remove_clip(self.clip)

        #t2 = time.perf_counter()
        #print("ADVANCE3: %s" % (t2 - t1))


    def stop(self):
        """
        Stop this clip/player making sure to send any midi off events
        """
        for event in self.left_to_play:
            if event.type == NOTE_OFF:
                self.engine.play(event, 0)
        self.left_to_play = []


    def start(self):
        """
        Stop the clip if already playing, then configure the play head to read from the start of the clip.
        This isn't a directly usable API, use MultiPlayer instead.
        """
        self.stopped = False
        if self.left_to_play is not None:
            self.stop()
        self.time_index = 0
        self.left_to_play = [ n for n in self.events ]
