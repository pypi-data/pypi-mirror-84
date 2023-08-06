from enum import Enum


class JobStatus(Enum):
    READY = (1, 'Job is ready!')
    PENDING = (2, 'Job is pending!')
    IN_PROGRESS = (3, 'Job is in progress!')
    FINISHED = (4, 'Job is finished!')

    def __new__(cls, member_value, member_phrase):
        member = object.__new__(cls)

        member._value_ = member_value
        member.phrase = member_phrase

        return member


class Pump:
    """ A pump component for  """


class Assembly:
    """ A collection of Component objects """



