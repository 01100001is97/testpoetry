from Core.ABCSkill import PassiveSkill, SkillAdvance, OnPressSkill, KeydownSkill, AutomateActivativeSkill
from Core.SpecElements import SpecVector, CoreStat, CreateSpecVector
from Skill.Attributes import *
import math


#class 아처_마스터리


class 크리티컬_샷(PassiveSkill, BuffAttribute):
    def __init__(self, level=20):
        max_level = 20
        stat = SpecVector()
        stat[CoreStat.CRITICAL_PERCENTAGE] = (2 * level)
        
        PassiveSkill.__init__(self=self, advanced=SkillAdvance.First, level=level, max=max_level)
        BuffAttribute.__init__(self=self, stat=stat)

# 2차


class 샤프_아이즈(OnPressSkill, BuffAttribute, BuffDurationAttribute, CombatOrdersAttribute):
    def __init__(self, level=30):
        max = 30
        stat = self.GetBuff(level=level)
        sharpDuration = 210 + 3 * level
        SharpIcon = None
        OnPressSkill.__init__(self=self, advanced=SkillAdvance.First, level=level, max=max, icon=SharpIcon)
        BuffAttribute.__init__(self=self, stat=stat)
        BuffDurationAttribute.__init__(self=self, duration=sharpDuration)
        CombatOrdersAttribute.__init__(self)

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
        self._BuffStat = self.GetBuff(level=level)

    def GetBuff(self, level):
        stat = SpecVector()
        stat[CoreStat.CRITICAL_PERCENTAGE] = 5 + math.ceil(level/2)
        stat[CoreStat.CRITICAL_DAMAGE] = math.ceil(level/2)


    
class 가이디드_에로우(OnPressSkill, DamageAttribute, SummonAttribute):
    def __init__(self, level=30):
        max = 30
        ArrowIcon = None
        ArrowDamage = 880
        ArrowAttackLine = 1
        ArrowAttackCount = 1

        OnPressSkill.__init__(
            self=self,
            icon=ArrowIcon,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )
        SummonAttribute.__init__(
            self=self,
            duration=Cooldown(minutes=9999),
            interval=Cooldown(milliseconds=600),
            mult=False
        )
        DamageAttribute.__init__(
            self=self,
            damage_point=ArrowDamage,
            line=ArrowAttackLine

        )
        
    def UseSkill(self):
        
        ArrowLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = SpecVector())
        return [ArrowLog]
    
class 이볼브(OnPressSkill, DamageAttribute, SummonAttribute, CooldownAttribute, SkillDelayAttribute):
    def __init__(self, level=30):
        max = 30
        EvolveIcon = None
        EvolveDamage = 450+15*level
        EvolveInterval = Cooldown(seconds=3)
        EvolveDelay = Cooldown(milliseconds=600)
        EvolveDuration = Cooldown(seconds=40)
        EvolveCooldown = Cooldown(seconds=120-math.floor(level/2))
        EvloveAttackLine = 7
        OnPressSkill.__init__(
            self=self,
            icon=EvolveIcon,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )
        SummonAttribute.__init__(
            self=self,
            duration=EvolveDuration,
            interval=EvolveInterval,
            mult=False
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=EvolveCooldown,
            isresetable=False
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=EvolveDelay,
            applyAttackSpeed=False
        )
        DamageAttribute.__init__(
            self=self,
            damage_point=EvolveDamage,
            line=EvloveAttackLine
        )

    def UseSkill(self):
         
        EvloveLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = SpecVector())
        return [EvloveLog]
    
        





