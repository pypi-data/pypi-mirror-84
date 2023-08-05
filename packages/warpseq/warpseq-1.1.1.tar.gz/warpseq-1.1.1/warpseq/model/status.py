import time

PREVIOUS = dict(
    tracks = {},
    devices = {},
    instruments = {},
    patterns = {},
    scales = {},
    clips = {},
    transforms = {},
    scenes = {},
    data_pools = {},
)

CURRENT = None

CATEGORIES = [ 'clips', 'tracks', 'devices', 'instruments', 'patterns', 'scales', 'transforms', 'scenes', 'data_pools' ]

def status_report(song, now=None, threshold=1):

    global PREVIOUS, CURRENT

    if CURRENT:
        PREVIOUS = CURRENT

    if now is None:
        now = time.perf_counter()

    slow = now - threshold

    status = dict(
        tracks = {},
        devices = {},
        instruments = {},
        patterns = {},
        scales = {},
        clips = {},
        transforms = {},
        scenes = {},
        data_pools = {},
    )

    for x in song.all_clips():
        status['clips'][x.obj_id] = x._played_ts and x._played_ts > slow

    for x in song.tracks:
        status['tracks'][x.obj_id] = x._played_ts and x._played_ts > slow

    for x in song.scenes:
        status['scenes'][x.obj_id] = x._played_ts and x._played_ts > slow

    for x in song.devices.values():
        status['devices'][x.obj_id] = x._played_ts and x._played_ts > slow

    for x in song.instruments.values():
        status['instruments'][x.obj_id] = x._played_ts and x._played_ts > slow

    for x in song.patterns.values():
        status['patterns'][x.obj_id] = x._played_ts and x._played_ts > slow

    for x in song.scales.values():
        status['scales'][x.obj_id] = x._played_ts and x._played_ts > slow

    for x in song.transforms.values():
        status['transforms'][x.obj_id] = x._played_ts and x._played_ts > slow

    for x in song.data_pools.values():
        status['data_pools'][x.obj_id] = x._played_ts and x._played_ts > slow

    playing = {}

    CURRENT = status

    for category in CATEGORIES:
        playing[category] = []

        entries = status[category]
        for (k,v) in entries.items():
            if v:
                playing[category].append(k)

    changes = _changes()

    result = dict(playing=playing, status=status, new_playing=changes['new_playing'], new_stopped=changes['new_stopped'])

    return result

def _changes():

    global CURRENT, PREVIOUS, CATEGORIES

    new_playing = {}
    new_stopped = {}

    for category in CATEGORIES:

        new_playing[category] = []
        new_stopped[category] = []

        previous_dict = PREVIOUS[category]
        current_dict  = CURRENT[category]


        for (obj_id, status) in current_dict.items():

            current_status = status
            previous_status = previous_dict.get(obj_id, None)

            if current_status != previous_status:
                if current_status:
                    new_playing[category].append(obj_id)
                else:
                    new_stopped[category].append(obj_id)

    return dict(new_playing=new_playing, new_stopped=new_stopped)