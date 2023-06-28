from Core.ABCSkill import PassiveSkill, SkillAdvance, OnPressSkill, KeydownSkill, AutomateActivativeSkill
from Core.SpecElements import SpecVector, CoreStat, CreateSpecVector
from Skill.Attributes import *
import math

# 1차 스킬
class MP증가(PassiveSkill, BuffAttribute):
    def __init__(self, level=20):
        max = 20
        stat = SpecVector()
        stat[CoreStat.STAT_MP_PERCENTAGE] = level
        stat[CoreStat.STAT_MP] = 20+5*level

        # 추후 변경점: 완드 착용시 크확 5% 증가

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.First, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)

    def DeleteBuff(self):
        pass

# 매직 가드, 에너지 볼트, 텔레포트, 마나 웨이브, 매직 아머

# 4차 스ㄹ

class 마스터_매직(PassiveSkill, BuffAttribute, BuffDurationAttribute, CombatOrdersAttribute):
    def __init__(self, level = 10):

        max = 10

        buff = self.SetBuffDuration(level)
        spell = self.SetSpell(level)

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Fourth, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=spell)
        BuffDurationAttribute.__init__(self=self, duration=buff)
        CombatOrdersAttribute.__init__(self=self)

    def SetSpell(self, level:int):
        return CreateSpecVector([CoreStat.ATTACK_SPELL], 3*level)
    
    def SetBuffDuration(self, level:int):
        return 5*level
    
    @property
    def Level(self):
        return self._level
    
    @Level.setter
    def Level(self, level:int):
        if not isinstance(level, int) or level < 0:
            raise ValueError("Level must be a non-negative integer")
        if level > self.MaxLevel:
            self._level = level
        self._level = level
        self.BuffDurationOption = self.SetBuffDuration(level=level)
        self._BuffStat = self.SetSpell(level=level)


class 아케인_에임(PassiveSkill, BuffAttribute, CombatOrdersAttribute):
    def __init__(self, level = 30):
        max = 30

        buff = self.SetBuffStat(level)

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Fourth, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=buff)
        CombatOrdersAttribute.__init__(self=self)

    def SetBuffStat(self, level:int):
        result = SpecVector()
        result[CoreStat.DAMAGE_PERCENTAGE] = (2+math.floor(level/5))*5
        result[CoreStat.IGNORE_GUARD_PERCENTAGE] = 5 + math.ceil(level/2)
    

    @property
    def Level(self):
        return self._level
    
    @Level.setter
    def Level(self, level:int):
        if not isinstance(level, int) or level < 0:
            raise ValueError("Level must be a non-negative integer")
        if level > self.MaxLevel:
            self._level = level
        self._level = level

        self._BuffStat = self.SetBuffStat(level=level)
        
        