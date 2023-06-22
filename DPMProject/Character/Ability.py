from enum import Enum

ABILITY_SLOT_MAX = 3

class CharacterAbilityEnum(Enum):
    BuffDuration = (25, 38, 50)
    PanicDamage = (5, 8, 10)
    CriticalProp = (10, 20, 30)
    BossDamage = (None, 10, 20)
    CooldownReset = (None, 10, 20)
    PassiveLevel = (None, None, 1)
    TargetExtension = (None, None, 1)
