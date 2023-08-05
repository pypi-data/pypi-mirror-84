# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

# custom exception types for easier capture of specific errors

# TODO: verify we are using all of these and consolidate

class WarpException(Exception):
    pass

class NotFound(WarpException):
    pass

class AlreadyExists(WarpException):
    pass

class InvalidInput(WarpException):
    pass

class RequiredInput(WarpException):
    pass

class InvalidExpression(InvalidInput):
    pass

class InvalidNote(InvalidInput):
    pass

class InvalidChord(InvalidInput):
    pass

class UnexpectedError(WarpException):
    pass

class ConfigError(WarpException):
    pass

class MIDIConfigError(WarpException):
    pass

class InvalidUsage(WarpException):
    pass

class TimeoutException(WarpException):
    pass

class InvalidOpcode(WarpException):
    pass

class StopException(WarpException):
    pass

class WebSlotCompilerException(WarpException):

    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        # TODO: this isn't surfaced anywhere, eliminate or surface them.
        return "Web Slot Compile Failed: %s" % (self.errors)
