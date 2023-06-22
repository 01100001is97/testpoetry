from abc import ABC, abstractmethod
from Core.Cooldown import Cooldown
from enum import Enum
from typing import Callable, Any


class SkillAdvance(Enum):
    """전직 차수를 의미함.

    Args:
        Enum (int): 스킬의 전직 횟수
    """
    Zero = 0
    First = 1
    Second = 2
    Third = 3
    Fourth = 4
    Hyper = 4.5
    Fifth = 5
    Sixth = 6


class Skill(ABC):
    """
    스킬을 추상화한 클래스. 모든 스킬 클래스는 이 클래스를 상속받아야 합니다.

    속성:
        _Advanced (SkillAdvance): 스킬의 등급(0~6차)을 나타내는 객체입니다.
        _level (int): 스킬의 현재 레벨을 나타냅니다.
        _MaxLevel (int): 스킬의 최대 레벨을 나타냅니다.
        _Owner (ABCCharacter): 스킬의 소유자를 나타냅니다.
        _Target (any): 스킬의 타겟을 나타냅니다.

    Args:
        advanced (SkillAdvance): 스킬의 등급(1차 2차 3차 스킬)을 나타냅니다.
        level (int): 스킬의 현재 레벨을 나타냅니다.
        max (int): 스킬의 최대 레벨을 설정합니다.
        target (any): 스킬의 타겟을 설정합니다.
    """
    _Advanced: SkillAdvance              
    _Level: int
    _MaxLevel: int
    _Owner: any
    _Target: any
    def __init__(self, advanced:SkillAdvance, level:int, max: int):
        self._Advanced = advanced
        self._level = level
        self._MaxLevel = max
        self._Target = None
        self._Owner = None

    @property
    def Advanced(self):
        return self._Advanced

    @Advanced.setter
    def Advanced(self, advanced: SkillAdvance):
        # 검사 로직: 여기에서는 advanced가 SkillAdvance의 인스턴스인지 확인합니다.
        if not isinstance(advanced, SkillAdvance):
            raise ValueError("Advanced must be an instance of SkillAdvance")
        self._Advanced = advanced

    @property
    def Level(self):
        return self._level

    @Level.setter
    def Level(self, level: int):
        # 검사 로직: 여기에서는 level이 0 이상의 정수인지 확인합니다.
        if not isinstance(level, int) or level < 0:
            raise ValueError("Level must be a non-negative integer")
        self._level = level

    @property
    def MaxLevel(self):
        return self._MaxLevel

    @MaxLevel.setter
    def MaxLevel(self, max: int):
        # 검사 로직: 여기에서는 max가 level보다 큰 정수인지 확인합니다.
        if not isinstance(max, int) or max < self.Level:
            raise ValueError("MaxLevel must be a integer greater than level")
        self._MaxLevel = max

    @property
    def Owner(self):
        return self._Owner

    @Owner.setter
    def Owner(self, owner: any):
        # 검사 로직: 여기에서는 owner가 ABCCharacter의 인스턴스인지 확인합니다.
        #if owner is not None and not isinstance(owner, ABCCharacter):
        #    raise ValueError("Owner must be an instance of ABCCharacter")
        self._Owner = owner

    @property
    def Target(self):
        return self._Target

    @Target.setter
    def Target(self, target: any):
        self._Target = target
        
    

#-------------------- 패시브 스킬 -------------------------
class PassiveSkill(Skill):
    """
    단순 패시브 스킬을 나타내는 클래스입니다.

    Args:
        Skill (class): 스킬 클래스를 상속받습니다.
    """
    def __init__(self, advanced:SkillAdvance, level:int, max:int):
        Skill.__init__(self=self, advanced=advanced, level=level, max=max)

    def SetTarget(self, target: any):
        if target is not None:
            self._Target = target
        else:
            raise ValueError("스킬 타겟 입력값이 None")
    
    def ApplySkill(self):
        #if isinstance(self._Owner, ABCCharacter) and self._Owner is not None:
        self._Target = self._Owner
        #else:
        #    raise AttributeError("스킬의 소유자를 먼저 설정해야함.")
        self.SetTarget(target=self._Owner)


class AutomateActivativeSkill(Skill):
    """
    공격 시 조건에 따라 자동으로 활성화 되는 스킬을 구현한 클래스입니다. 람다 함수를 이용하여 조건을 설정합니다.

    Args:
        advanced (SkillAdvance): 스킬의 등급을 설정합니다.
        level (int): 스킬의 현재 레벨을 설정합니다.
        max (int): 스킬의 최대 레벨을 설정합니다.
        activator (lambda: False): 스킬의 활성화 여부를 결정하는 람다 함수입니다. 기본값은 항상 False를 반환하는 람다 함수입니다.
        target (any): 스킬의 타겟을 설정합니다. 기본값은 None입니다.
    """
    _Activator: lambda: False

    def __init__(self, advanced: SkillAdvance, level: int, max: int, activator: lambda: False, target=any ):
        self.Activator = activator
        Skill.__init__(advanced, level, max, target)

    @property
    def Activator(self):
        return self._Activator

    @Activator.setter
    def Activator(self, activator: Callable[[None], bool]):
        if not callable(activator):
            raise ValueError("Activator must be callable.")
        self._Activator = activator


#class OnHitActivate(AutomateActivate):
#    pass

#-------------------- 액티브 스킬 -------------------------
class ActiveSkill(Skill):
    """
    사용자의 입력에 의해 활성화되는 스킬을 구현한 클래스입니다.

    Args:
        icon (any): 스킬 아이콘을 설정합니다. 기본값은 None입니다.
        advanced (SkillAdvance): 스킬의 등급을 설정합니다.
        level (int): 스킬의 현재 레벨을 설정합니다.
        max (int): 스킬의 최대 레벨을 설정합니다.
        target (any): 스킬의 타겟을 설정합니다. 기본값은 None입니다.
    """
    _Icon: None

    def __init__(self, icon, advanced: SkillAdvance, level: int, max: int, target= any):
        self.Icon = icon
        Skill.__init__(advanced, level, max, target)

    @property
    def Icon(self):
        return self._Icon

    @Icon.setter
    def Icon(self, icon: Any):
        # 이 부분은 나중에 아이콘에 대한 검증 로직을 추가할 수 있습니다.
        self._Icon = icon

    @abstractmethod
    def UseSkill(self, **kwargs):
        pass

class OnPressSkill(ActiveSkill):
    """
    키 입력에 따라 활성화되는 스킬을 구현한 클래스입니다.

    Args:
        icon (any): 스킬 아이콘을 설정합니다. 기본값은 None입니다.
        advanced (SkillAdvance): 스킬의 등급을 설정합니다.
        level (int): 스킬의 현재 레벨을 설정합니다.
        max (int): 스킬의 최대 레벨을 설정합니다.
        target (any): 스킬의 타겟을 설정합니다. 기본값은 None입니다.
    """
    def __init__(self, icon, advanced: SkillAdvance, level: int, max: int, target =any):
        ActiveSkill.__init__(self, icon, advanced= advanced, level=level , max=max, target=target)

class KeydownSkill(ActiveSkill):
    """
    키를 계속 누르고 있을 때 활성화되는 스킬을 구현한 클래스입니다.

    Args:
        icon (any): 스킬 아이콘을 설정합니다. 기본값은 None입니다.
        advanced (SkillAdvance): 스킬의 등급을 설정합니다.
        level (int): 스킬의 현재 레벨을 설정합니다.
        max (int): 스킬의 최대 레벨을 설정합니다.
        target (any): 스킬의 타겟을 설정합니다. 기본값은 None입니다.
    """
    def __init__(self, icon, advanced: SkillAdvance, level: int, max: int, keydowntime: Cooldown, target = any):
        self.KeydownTime = keydowntime
        ActiveSkill.__init__(self, icon, advanced=advanced, max=max, level=level, target=target)

    @property
    def KeydownTime(self):
        return self._KeydownTime
    
    @KeydownTime.setter
    def KeydownTime(self, time:Cooldown):
        if not isinstance(time, Cooldown):
            raise ValueError("time must be a Cooldown")
        
        if time < Cooldown(seconds = 0):
            raise ValueError("time can't be negative")
        
        self._KeydownTime = time