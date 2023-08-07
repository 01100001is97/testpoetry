from abc import ABC, abstractmethod
from Core.Cooldown import Cooldown
from enum import Enum
from typing import Callable, Any
from datetime import timedelta
from Core.SpecElements import SpecVector, CoreStat
class SkillAdvance(Enum):
    """전직 차수를 의미함.

    Args:
        Enum (int): 스킬의 전직 횟수
    """
    Zero = 0
    First = 5
    Second = 4
    Third = 3
    Fourth = 2
    Hyper = 2
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
    def Owner(self, owner):
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
        
    
    def __str__(cls):
        repr_string = repr(cls)
        if '대기' in repr_string:
            return '0.01초 대기중'

        class_list = cls.mro()
        class_string = class_list[-2].__name__ if len(class_list) > 1 else class_list[0].__name__
        return class_string

    @property
    def Name(self):
        class_string = self.__class__.__name__
        split_string = class_string.split(".")
        split_string = split_string[-1].rstrip('>')
        
        return split_string.replace('_', ' ')
        

    
    
    

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

    # TODO:이전 스킬들(패스파인더, 썬콜)에 대한 기능 테스트가 필요함
    def ApplyPassiveLevel1(self):
        if self.Advanced == SkillAdvance.Fourth:
            self.MaxLevel += 1
            self.Level += 1



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
    

    def __init__(self, advanced: SkillAdvance, level: int, max: int):    
        Skill.__init__(self,advanced=advanced, level=level, max=max)

    @abstractmethod
    def active(self):
        pass

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
    Done: bool

    def __init__(self, icon, advanced: SkillAdvance, level: int, max: int, target= any):
        self.Icon = icon
        self._Done = False
        Skill.__init__(self, advanced, level, max)

    @property
    def Done(self):
        return self._Done
    
    @Done.setter
    def Done(self, b:bool):
        if not isinstance(b, bool):
            raise TypeError("b must be a bool type")
        
        self._Done = b

    @property
    def Icon(self):
        return self._Icon

    @Icon.setter
    def Icon(self, icon: Any):
        # 이 부분은 나중에 아이콘에 대한 검증 로직을 추가할 수 있습니다.
        self._Icon = icon

    @abstractmethod
    def UseSkill(self):
        # 공격 스킬의 경우 무기 상수, 직업 보정 상수,방무 고려해야함
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
    def __init__(self, icon, advanced: SkillAdvance, level: int, max: int):
        ActiveSkill.__init__(self, icon, advanced= advanced, level=level , max=max)

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
    def __init__(self, icon, advanced: SkillAdvance, level: int, max: int, keydowntime: Cooldown):
        self.KeydownTime = keydowntime
        ActiveSkill.__init__(self, icon, advanced=advanced, max=max, level=level)

    @abstractmethod
    def Finish(self):
        pass

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


class OriginSkill(OnPressSkill):
    def __init__(self, icon, advanced: SkillAdvance, level: int, max: int, timingTable:list):
        self.TimingTable = timingTable
        self.index = 0
        
        OnPressSkill.__init__(self, icon, advanced, level, max)

    @classmethod
    def CalculateBossDamage(self,level):
        sv = SpecVector()
        if level >= 30:
            sv[CoreStat.DAMAGE_PERCENTAGE_BOSS] = 30
        elif level >= 10:
            sv[CoreStat.DAMAGE_PERCENTAGE_BOSS] = 20
        return sv
        
    @classmethod
    def CalculateIgnoreGuard(self, level):
        sv = SpecVector()
        if level >= 30:
            sv[CoreStat.IGNORE_GUARD_PERCENTAGE] = 30
        elif level >= 10:
            sv[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20
        return sv