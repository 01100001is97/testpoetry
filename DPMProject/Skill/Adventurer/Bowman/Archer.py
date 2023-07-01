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

class 에인션트_보우_액셀레이션(PassiveSkill, BuffAttribute):
    def __init__(self, level=10):
        max = 10
        stat = SpecVector()
        stat[CoreStat.STAT_DEX] = 2* level
        
        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Second, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)


class 에인션트_보우_마스터리(PassiveSkill, BuffAttribute):
    # 마스터리 상승으로 되어있으나, 에인션트_보우_엑스퍼트 스킬에서 오르는 수치로 재조정되므로 패스함
    def __init__(self, level=10):
        max = 10
        stat = SpecVector()
        stat[CoreStat.ATTACK_PHYSICAL] = 3 * level
        

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Third, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)
       




class 에인션트_가이던스(PassiveSkill, BuffAttribute, DurationAttribute):
    def __init__(self, level=10):
        max = 10
        stat = SpecVector()
        stat[CoreStat.STAT_HP_PERCENTAGE] = 50
        stat[CoreStat.FINAL_DAMAGE_PERCENT] = 2 * level
        self._AncientGuidance = 0
        
        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Third, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)
        

class 에인션트_가이던스_버프(PassiveSkill, BuffAttribute, DurationAttribute):
    def __init__(self, level=10):
        max = 10
        stat = SpecVector()
        stat[CoreStat.FINAL_DAMAGE_PERCENT] = 8
        
        buffduration = Cooldown(seconds=40)
        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Third, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)
        DurationAttribute.__init__(
            self=self,
            duration=buffduration,
            serverlack=True,
            isbuffmult=False
        )

# 4차. 컴뱃오더스와 렙당 1의 효과를 받음
class 에센스_오브_아처(PassiveSkill, BuffAttribute, CombatOrdersAttribute):
    def __init__(self, level=10):
        max = 10
        stat = self.GetBuffStat(level)
       
        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Fourth, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)
        CombatOrdersAttribute.__init__(self=self)

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
        self._BuffStat = self.GetBuffStat(level=level)

    def GetBuffStat(self, level):
        stat = SpecVector()
        stat[CoreStat.CRITICAL_PERCENTAGE] = level
        stat[CoreStat.DAMAGE_PERCENTAGE] = level
        stat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 3 * level
        return stat

class 샤프_아이즈(OnPressSkill, BuffAttribute, BuffDurationAttribute, CombatOrdersAttribute):
    def __init__(self, level=30):
        max = 30
        stat = self.GetBuff(level=level)
        sharpDuration = 210 + 3 * level

        OnPressSkill.__init__(self=self, advanced=SkillAdvance.First, level=level, max=max)
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


class 에인션트_보우_엑스퍼트(PassiveSkill, BuffAttribute, CombatOrdersAttribute, MasteryAttribute):
    def __init__(self, level=30):
        max = 30
        stat = SpecVector()
        ancientMastery = self.set_mastery(level)
        
        stat[CoreStat.ATTACK_PHYSICAL] = self.set_attack_power(level)
        stat[CoreStat.CRITICAL_DAMAGE] = self.set_critical_damage(level=level)

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Fourth, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)
        CombatOrdersAttribute.__init__(self=self)
        MasteryAttribute.__init__(self=self, mastery= ancientMastery)

    def set_mastery(self, level:int):
        return 55 + math.ceil(level/2)

    def set_attack_power(self, level:int):
        return level * 2

    def set_critical_damage(self, level:int):
        return level

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
        self.Mastery = self.set_mastery(level)
        self._BuffStat[CoreStat.ATTACK_PHYSICAL] = self.set_attack_power(level)
        self._BuffStat[CoreStat.CRITICAL_DAMAGE] = self.set_critical_damage(level)

    
class 일루전_스탭(PassiveSkill, BuffAttribute, CombatOrdersAttribute):
    def __init__(self, level=30):
        max = 30
        stat = SpecVector()
        stat[CoreStat.STAT_DEX] = self.set_agility(level)

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Fourth, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)
        CombatOrdersAttribute.__init__(self)

    def set_agility(self, level:int):
        return 20 + 3*level

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
        self._BuffStat[CoreStat.STAT_DEX] = self.set_agility(level=level)


class 어드밴스드_카디널_포스(PassiveSkill, CombatOrdersAttribute):

    def __init__(self, level=21):
        self.Level = level
        max = 21
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max
        )
        CombatOrdersAttribute.__init__(self)

    # Get the damage for Cardinal Discharge
    def GetCardinalDischargeDamage(self):
        return 200+5*self.Level
    
    # Get the number of attack lines for Cardinal Discharge
    def GetCardinalDischargeAttackLine(self):
        return 5

    # Get the number of attack count for Cardinal Discharge
    def GetCardinalDischargeAttackCount(self):
        return 2

    # Get the damage for Cardinal Blast
    def GetCardinalBlastDamage(self):
        return 300+15*self.Level

    # Get the number of attack lines for Cardinal Blast
    def GetCardinalBlastAttackLine(self):
        return 5

    # Get the number of attack count for Cardinal Blast
    def GetCardinalBlastAttackCount(self):
        return 1

    # Get the damage for Cardinal Transition
    def GetCardinalTransitionDamage(self):
        return 400 + 7 * self.Level

    # Get the number of attack lines for Cardinal Transition
    def GetCardinalTransitionAttackLine(self):
        return 5
    # Get the number of attack count for Cardinal Transition
    def GetCardinalTransitionAttackCount(self):
        return 1
    
class 에디셔널_트랜지션(PassiveSkill, BuffAttribute, CombatOrdersAttribute):
    def __init__(self, level= 20):
        max = 20
        BuffStat= self.GetAtkPer(level)
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max
        )
        BuffAttribute.__init__(
            self=self,
            stat=BuffStat
        )
        CombatOrdersAttribute.__init__(self)

    def GetAtkPer(self, level):
        return CreateSpecVector([CoreStat.ATTACK_PHYSICAL_PERCENTAGE], level)
    
    @property
    def Level(self):
        return super().Level
    
    # Skill 의 Level setter 재정의 - 스킬 레벨의 변화와 데미지 계산 바인딩
    @Level.setter
    def Level(self, level:int):
        # 검사 로직: 여기에서는 level이 0 이상의 정수인지 확인합니다.
        if not isinstance(level, int) or level < 0:
            raise ValueError("Level must be a non-negative integer")
        # 추가 로직: level이 MaxLevel 보다 큰 경우 값을 절삭함
        if level > self.MaxLevel:
            self._level = level
        self._level = level

        self.BuffStat = self.GetAtkPer(level)

    
class 에인션트_아처리(PassiveSkill, CombatOrdersAttribute):
    def __init__(self, level=30):
        max = 30
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max
        )
        CombatOrdersAttribute.__init__(self=self)

    def AdditionalDischargeDamageUpgrade(self, level=31):
        return 35 + level
    
    def AdditionalBlastDamageUpgrade(self, level=31):
        return 40 + level
    
    # 스플릿 미스텔 패스함
        
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
    
        





