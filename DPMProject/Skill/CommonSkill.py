from Core.ABCSkill import PassiveSkill, AutomateActivativeSkill, OnHitActivate, SkillAdvance, SkillAdvance, OnPressSkill
from Attributes import *
from Core.SpecElements import SpecVector, CoreStat, CreateSpecVector
from Item.ItemGroup import Weapon

##-------------- 액티브 -------------------

class 연합의_의지(PassiveSkill, BuffAttribute):
    def __init__(self):
        passiveStat = SpecVector()
        passiveStat[CoreStat.STAT_ALL] = 5
        passiveStat[CoreStat.ATTACK_PHYSICAL] = 5
        passiveStat[CoreStat.ATTACK_SPELL] = 5
        PassiveSkill(advanced=SkillAdvance.Zero, level=1, max=1)
        BuffAttribute(stat=passiveStat)

# 패시브 스킬은 아니지만, DPM 계산 상 무한지속으로 간주
class 영웅의_메아리(PassiveSkill, BuffAttribute):
    def __init__(self):
        echoStat = SpecVector()
        echoStat[CoreStat.ATTACK_PHYSICAL_PERCENTAGE] = 4
        echoStat[CoreStat.ATTACK_SPELL_PERCENTAGE] = 4
        PassiveSkill(advanced=SkillAdvance.Zero, level=1, max=1)
        BuffAttribute(stat=echoStat)

class 여제의_축복(PassiveSkill, BuffAttribute):
    def __init__(self):
        level = 30
        passiveStat = SpecVector()
        passiveStat[CoreStat.ATTACK_PHYSICAL] = level
        passiveStat[CoreStat.ATTACK_SPELL] = level
        PassiveSkill.__init__(advanced=SkillAdvance.Zero, level=level, max=30)
        BuffAttribute.__init__(stat=passiveStat)

# 패시브 스킬은 아니지만, DPM 계산 상 무한지속으로 간주
class 고급_무기_제련(PassiveSkill, BuffAttribute):
    def __init__(self):
        enchantStat = SpecVector()
        enchantStat[CoreStat.CRITICAL_DAMAGE] = 5
        PassiveSkill.__init__(advanced=SkillAdvance.Zero,level=1, max=1)
        BuffAttribute.__init__(stat=enchantStat)

class 파괴의_얄다바오트(PassiveSkill, BuffAttribute):
    def __init__(self):
        enchantStat = SpecVector()
        enchantStat[CoreStat.FINAL_DAMAGE_PERCENT] = 10
        PassiveSkill.__init__(advanced=SkillAdvance.Zero, level=1, max=1)
        BuffAttribute.__init__(stat=enchantStat)
        
class 마약_버프(PassiveSkill, BuffAttribute):
    def __init__(self):
        passiveStat = SpecVector()
        # 마약 수치에 따라서 적용
        PassiveSkill.__init__(advanced=SkillAdvance.Zero,level=1, max=1)
        BuffAttribute.__init__(stat=passiveStat)

##-------------- 액티브 -------------------

class 리스트레인트링(OnPressSkill, BuffAttribute, CooldownAttribute, DurationAttribute, SkillDelayAttribute):
    def __init__(self, level: int):
        buffStat = SpecVector()
        
        buffStat[CoreStat.ATTACK_PHYSICAL_PERCENTAGE] = level*25
        OnPressSkill.__init__(self=self, icon=None, advanced=SkillAdvance.Zero, level=level, max=4)
        BuffAttribute.__init__(self=self, stat=buffStat)
        CooldownAttribute.__init__(self=self, cooldown=Cooldown(minutes=3))
        DurationAttribute.__init__(self=self, duration=Cooldown(seconds=15), serverlack=False, isbuffmult=False)
        SkillDelayAttribute.__init__(self=self, casting_delay=Cooldown(miliseconds=30))

class 웨폰퍼프_I링(OnPressSkill, BuffAttribute, CooldownAttribute, DurationAttribute, SkillDelayAttribute):
    def __init__(self, level: int, weapon: Weapon):
        multStat = SpecVector()
        weaponSpec, _ = weapon.TotalSpec()
        
        multStat[CoreStat.STAT_INT] = weaponSpec[CoreStat.ATTACK_SPELL] * level

        OnPressSkill.__init__(self=self, icon=None, advanced=SkillAdvance.Zero, level=level, max=4)
        BuffAttribute.__init__(self=self, stat=multStat)
        CooldownAttribute.__init__(self=self, cooldown=Cooldown(minutes=3))
        DurationAttribute.__init__(self=self, duration=Cooldown(seconds=15), serverlack=True, isbuffmult=False)
        SkillDelayAttribute.__init__(self=self, casting_delay=Cooldown(miliseconds=30))

class 웨폰퍼프_D링(OnPressSkill, BuffAttribute, CooldownAttribute, DurationAttribute, SkillDelayAttribute):
    def __init__(self, level: int, weapon: Weapon):
        multStat = SpecVector()
        weaponSpec, _ = weapon.TotalSpec()
        
        multStat[CoreStat.STAT_DEX] = weaponSpec[CoreStat.ATTACK_PHYSICAL] * level

        OnPressSkill.__init__(self=self, icon=None, advanced=SkillAdvance.Zero, level=level, max=4)
        BuffAttribute.__init__(self=self, stat=multStat)
        CooldownAttribute.__init__(self=self, cooldown=Cooldown(minutes=3))
        DurationAttribute.__init__(self=self, duration=Cooldown(seconds=15), serverlack=True, isbuffmult=False)
        SkillDelayAttribute.__init__(self=self, casting_delay=Cooldown(miliseconds=30))

class 웨폰퍼프_S링(OnPressSkill, BuffAttribute, CooldownAttribute, DurationAttribute, SkillDelayAttribute):
    def __init__(self, level: int, weapon: Weapon):
        multStat = SpecVector()
        weaponSpec, _ = weapon.TotalSpec()

        multStat[CoreStat.STAT_STR] = weaponSpec[CoreStat.ATTACK_PHYSICAL] * level

        OnPressSkill.__init__(self=self, icon=None, advanced=SkillAdvance.Zero, level=level, max=4)
        BuffAttribute.__init__(self=self, stat=multStat)
        CooldownAttribute.__init__(self=self, cooldown=Cooldown(minutes=3))
        DurationAttribute.__init__(self=self, duration=Cooldown(seconds=15), serverlack=True, isbuffmult=False)
        SkillDelayAttribute.__init__(self=self, casting_delay=Cooldown(miliseconds=30))

class 웨폰퍼프_L링(OnPressSkill, BuffAttribute, CooldownAttribute, DurationAttribute, SkillDelayAttribute):
    def __init__(self, level: int, weapon: Weapon):
        multStat = SpecVector()
        weaponSpec, _ = weapon.TotalSpec()

        multStat[CoreStat.STAT_LUK] = weaponSpec[CoreStat.ATTACK_PHYSICAL] * level

        OnPressSkill.__init__(self=self, icon=None, advanced=SkillAdvance.Zero, level=level, max=4)
        BuffAttribute.__init__(self=self, stat=multStat)
        CooldownAttribute.__init__(self=self, cooldown=Cooldown(minutes=3))
        DurationAttribute.__init__(self=self, duration=Cooldown(seconds=15), serverlack=True, isbuffmult=False)
        SkillDelayAttribute.__init__(self=self, casting_delay=Cooldown(miliseconds=30))
