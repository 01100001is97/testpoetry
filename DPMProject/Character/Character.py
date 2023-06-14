from Core.SpecElements import *
from Core.ABCItem import ItemParts
from abc import ABC, abstractmethod
from Core.Job import JobType
from Character.CharacterAbility import CharacterAbility
from Character.Trait import TraitStat, TraitBuffDuration
from Farm import Monster
from typing import Dict
from enum import Enum


class ItemSlot(Dict[ItemParts, object]):
    def __init__(self):
        super().__init__()

    def add_item(self, part: ItemParts, item: object):
        self[part] = item

    def remove_item(self, part: ItemParts):
        if part in self:
            del self[part]

    def get_item(self, part: ItemParts):
        return self.get(part, None)

   

class ABCCharacter(ABC):
    """캐릭터 기본 클래스로, 캐릭터들이 공통적으로 가지고 있는 기능들 묘사

    Args:
        ABC (_type_): _description_
    Level:int
    """    
    _Level: int
    _HyperStatPoint:int
    _Job:JobType
    _Cooldown:int
    _CooldownPercent:int
    _ItemSlot: ItemSlot
    _AbilitySlot: CharacterAbility
    _BuffDuration: list[int]
    _SummonDuration: list[int]
    # 성향은 만렙으로 가정함.
    PersonalTrait: SpecVector
    # 미구현(모도 링크같은 것들때문에 specvector로 불가능)
    LinkSkillList: list[None]
    # 미구현(쿨감 등)
    Farm: list[None]
    # 미구현(스킬의 리스트로 설정)
    PetBuffList: list
    # 미구현(펫 버프, 펫장비, 펫효과)
    PetSlot: list[2]
    # 미구현(링크 스킬, 유니온(와헌), 0차, 1~5차 등)
    SkillList: list

    def __init__(self, level:int, job:JobType, itemslot: ItemSlot, ability:CharacterAbility):
        self.Level = level
        self.Job = job

    
pass