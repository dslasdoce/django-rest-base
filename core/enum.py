from core.serializers import IntFlag, IntFlagHandler
from enum import auto


class ClaimTypeEnum(IntFlag):
    achievement = auto()
    controversy = auto()
    advocacy = auto()


class ClaimType(IntFlagHandler):
    enum_class = ClaimTypeEnum
