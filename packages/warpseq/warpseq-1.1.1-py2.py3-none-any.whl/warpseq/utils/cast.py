# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

def safe_int(x, default=0):

    x = str(x)
    if x.endswith("."):
        x = x + ".0"
    if x.strip() == "":
        return default

    try:
        return int(x)
    except ValueError:
        return default

def safe_float(x, default=0):

    x = str(x)
    if x.endswith("."):
        x = x + ".0"
    if x.strip() == "":
        return default

    try:
        return float(x)
    except ValueError:
        return default

def safe_bool(x, default=False):

    y = str(x).lower()

    if y in [ "true", "yes", "y", "1" ]:
        return True
    if y in [ "false", "no", "n", "0" ]:
        return False

    try:
        x = float(x)
    except:
        return False

    if x > 1:
        return True
    if x < 0:
        return False
    return random.random() < x

