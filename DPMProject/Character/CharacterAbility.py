from enum import Enum

class CharacterAbilityEnum(Enum):
    BuffDuration = (25, 38, 50)
    PanicDamage = (5, 8, 10)
    CriticalProp = (10, 20, 30)
    BossDamage = (None, 10, 20)
    CooldownReset = (None, 10, 20)
    PassiveLevel = (None, None, 1)
    TargetExtension = (None, None, 1)


class CharacterAbilityGrade(Enum):
    Epic = 0
    Unique = 1
    Legendary = 2

class CharacterAbility:
    _option:CharacterAbilityEnum
    _grade: CharacterAbilityGrade

    def __init__(self, option:CharacterAbilityEnum,grade:CharacterAbilityGrade):
        self._option = option
        self._grade = grade

