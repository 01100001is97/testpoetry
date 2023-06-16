from abc import ABC, abstractmethod
from datetime import timedelta


class Cooldown:
    cooldown: timedelta

    def __init__(self, **kwargs):
        if "cooldown" in kwargs:
            cooldown = kwargs["cooldown"]
            if not isinstance(cooldown, timedelta):
                raise TypeError("cooldown must be a timedelta instance")
            self.cooldown = cooldown
        elif "seconds" in kwargs:
            seconds = kwargs["seconds"]
            self.cooldown = timedelta(seconds=seconds)
        elif "minutes" in kwargs:
            min = kwargs["minutes"]
            self.cooldown = timedelta(minutes=min) 
        else:
            raise ValueError("either 'cooldown' or 'seconds' argument must be provided")
    
    def __sub__(self, other):
        if isinstance(other, timedelta):
            return self.cooldown - other
        elif isinstance(other, Cooldown):
            return self.cooldown - other.cooldown
        else:
            raise TypeError("unsupported operand type(s) for -: 'SkillCooldown' and '{}'".format(type(other)))
    
    def __isub__(self, other):
        if isinstance(other, timedelta):
            self.cooldown -= other
        elif isinstance(other, Cooldown):
            self.cooldown -= other.cooldown
        else:
            raise TypeError("unsupported operand type(s) for -=: 'SkillCooldown' and '{}'".format(type(other)))
        return self
    
    def update(self):
        self.cooldown -= timedelta(microseconds=10)
    
    def __repr__(self):
        return "SkillCooldown({})".format(self.cooldown)



class ABCSkill(ABC):
    _Damage: int
    _Cooldown: Cooldown
    _AfterDelay: Cooldown
    _Target: None # 몬스터 클래스 만든 후 수정할 것.
    _Icon: None # 나중에 스킬 이미지 가져올거임
    
    _Level: int
    _SkillType: None # 나중에 추가.(keypress, keydown, combination)
# 지속시간, _AttackDelay: Cooldown
