from Core.ABCSkill import PassiveSkill, AutomateActivativeSkill, OnPressSkill, SkillAdvance
from Skill.Attributes import *
from Core.SpecElements import SpecVector, CoreStat, CreateSpecVector
from Core.Condition import ConditionEnum

MAX_LINK_SLOT = 13

class 임피리컬_널리지(PassiveSkill, DebuffAttribute):
    def __init__(self):
        skilllevel = 6
        passiveStat = SpecVector()
        passiveStat[CoreStat.DAMAGE_PERCENTAGE] = skilllevel
        passiveStat[CoreStat.IGNORE_GUARD_PERCENTAGE] = skilllevel
        PassiveSkill.__init__(self,advanced=SkillAdvance.Zero, level=skilllevel, max = 6)
        DebuffAttribute.__init__(self,debuff_stat=passiveStat, condition=[ConditionEnum.모험가법사])

    def DeleteDebuff(self):
        return super().DeleteDebuff()
        

class 어드벤쳐러_큐리어스(PassiveSkill, BuffAttribute):
    def __init__(self):
        skilllevel = 6
        passiveStat = SpecVector()
        passiveStat[CoreStat.CRITICAL_PERCENTAGE] = 10
        PassiveSkill.__init__(self,advanced=SkillAdvance.Zero, level=skilllevel, max= 6)
        BuffAttribute.__init__(self,stat=passiveStat)
    def DeleteBuff(self):
        return super().DeleteBuff()

class 시프_커닝(AutomateActivativeSkill, BuffAttribute, CooldownAttribute, DurationAttribute):
    def __init__(self):
        skilllevel = 6
        buffStat = SpecVector()
        buffStat[CoreStat.DAMAGE_PERCENTAGE] = skilllevel * 3

        duration = Cooldown(seconds=10)
        cooldown = Cooldown(seconds=20)

        AutomateActivativeSkill.__init__(
            self,
            advanced=SkillAdvance.Zero, 
            level= skilllevel,
            max=6,
            target=None,
            activator=lambda target: target.condition() # 적용할 때로 변경
            )
        BuffAttribute.__init__(self,stat=buffStat)
        CooldownAttribute.__init__(self,cooldown=cooldown,isresetable=False)
        DurationAttribute.__init__(
            self,
            duration=duration, 
            serverlack=True, 
            isbuffmult=False
            )
    def DeleteBuff(self):
        return super().DeleteBuff()
        
class 파이렛_블레스(PassiveSkill, BuffAttribute):
    def __init__(self):
        skilllevel = 6
        BuffStat = CreateSpecVector([CoreStat.STAT_ALL], (skilllevel+1)*10, [CoreStat.STAT_HP, CoreStat.STAT_MP], 175*(1+skilllevel))
        
        PassiveSkill.__init__(self,advanced=SkillAdvance.Zero, level=skilllevel, max=6)
        BuffAttribute.__init__(self,stat=BuffStat)
    def DeleteBuff(self):
        return super().DeleteBuff()

class 시그너스_블레스(PassiveSkill, BuffAttribute):
    def __init__(self):
        skilllevel = 10
        BuffStat = CreateSpecVector([CoreStat.ATTACK_PHYSICAL, CoreStat.ATTACK_SPELL], 5+2*skilllevel)

        PassiveSkill.__init__(self,advanced=SkillAdvance.Zero, level=skilllevel, max=10)
        BuffAttribute.__init__(self,stat=BuffStat)
    def DeleteBuff(self):
        return super().DeleteBuff()

class 하이브리드_로직(PassiveSkill, BuffAttribute):
    def __init__(self):
        skilllevel = 2
        BuffStat = CreateSpecVector([CoreStat.STAT_ALL_PERCENTAGE], 5*skilllevel)
        PassiveSkill.__init__(self,SkillAdvance.Zero, skilllevel, 2)
        BuffAttribute.__init__(self,stat=BuffStat)
    def DeleteBuff(self):
        return super().DeleteBuff()

class 데몬스_퓨리(PassiveSkill, BuffAttribute):
    def __init__(self):
        skilllevel = 2
        buffstat = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE_BOSS], 5*(1+skilllevel))

        PassiveSkill.__init__(self=self,advanced=SkillAdvance.Zero, level = skilllevel, max=2)
        BuffAttribute.__init__(self=self,stat=buffstat)
    def DeleteBuff(self):
        return super().DeleteBuff()

class 와일드_레이지(PassiveSkill, BuffAttribute):
    def __init__(self):
        skilllevel = 2
        buffstat = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE], 5*skilllevel)

        PassiveSkill.__init__(self=self,advanced=SkillAdvance.Zero, level = skilllevel, max=2)
        BuffAttribute.__init__(self=self, stat=buffstat)
    def DeleteBuff(self):
        return super().DeleteBuff()

class 퍼미에이트(PassiveSkill, BuffAttribute):
    def __init__(self):
        skilllevel = 2
        buffstat = CreateSpecVector([CoreStat.IGNORE_GUARD_PERCENTAGE], 5*(1+skilllevel))

        PassiveSkill.__init__(self,advanced=SkillAdvance.Zero, level = skilllevel, max=2)
        BuffAttribute.__init__(self, stat=buffstat)

    def DeleteBuff(self):
        return super().DeleteBuff()

class 데들리_인스팅트(PassiveSkill, BuffAttribute):
    def __init__(self):
        skilllevel = 2
        buffstat = CreateSpecVector([CoreStat.CRITICAL_PERCENTAGE], 5*(1+skilllevel))

        PassiveSkill.__init__(self,advanced=SkillAdvance.Zero, level = skilllevel, max=2)
        BuffAttribute.__init__(self,stat=buffstat)

    def DeleteBuff(self):
        return super().DeleteBuff()

class 아이언_윌(PassiveSkill, BuffAttribute):
    def __init__(self):
        skilllevel = 2
        buffstat = CreateSpecVector([CoreStat.STAT_HP_PERCENTAGE], 5*(1+skilllevel))

        PassiveSkill.__init__(self,advanced=SkillAdvance.Zero, level = skilllevel, max=2)
        BuffAttribute.__init__(self,stat=buffstat)

    def DeleteBuff(self):
        return super().DeleteBuff()

class 인텐시브_인설트(AutomateActivativeSkill, BuffAttribute):
    def __init__(self):
        skilllevel = 2
        conditionDamage = skilllevel*3
        underlevelDamage = skilllevel*3
        buffstat = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE], 1)

        AutomateActivativeSkill.__init__(
            self,
            advanced=SkillAdvance.Zero,
            level=skilllevel,
            max=2,
            activator=lambda owner, target: (conditionDamage if len(target.condition()) else 0) + (underlevelDamage if owner.GetLevel() > target.GetLevel() else 0),
            target=None
        )
        BuffAttribute.__init__(self,stat=buffstat)

    def DeleteBuff(self):
        return super().DeleteBuff()

class 소울_컨트랙트(OnPressSkill, BuffAttribute, DurationAttribute, CooldownAttribute):
    def __init__(self):
        iconSoul = None
        lev = 2
        duration = Cooldown(seconds=10)
        cooldown = Cooldown(seconds=90)

        buff = SpecVector()
        buff[CoreStat.DAMAGE_PERCENTAGE] = 15*(1+lev)

        OnPressSkill.__init__(
            self=self,
            icon=iconSoul,
            advanced=SkillAdvance.Zero,
            level=lev,
            max=2,
            target=None
        )
        BuffAttribute.__init__(self, stat=buff)
        DurationAttribute.__init__(self,duration=duration, serverlack=True, isbuffmult=True)
        CooldownAttribute.__init__(self, cooldown=cooldown, isresetable=True)

    def UseSkill(self, **kwargs):
        # 엔버면 버프 효과 2배
        return None
    
    def DeleteBuff(self):
        return super().DeleteBuff()
    
    
class 프라이어_프리퍼레이션(AutomateActivativeSkill, BuffAttribute, DurationAttribute, Cooldown, StackAttribute):
    def __init__(self):
        level = 2
        skillDuration = 20
        skillCooldown = 40
        buff = SpecVector()
        buff[CoreStat.DAMAGE_PERCENTAGE] = 1+8*level
        activeStack = 25

        AutomateActivativeSkill.__init__(
            self,
            advanced=SkillAdvance.Zero,
            level=level,
            max=2,
            activator= lambda stack: stack >= activeStack,
            target=self.Owner
        )
        BuffAttribute(self,stat=buff)
        DurationAttribute(self,duration=skillDuration, serverlack=True, isbuffmult=True)
        CooldownAttribute(self,cooldown=skillCooldown, isresetable=False)

    def DeleteBuff(self):
        return super().DeleteBuff()

class 노블레스(AutomateActivativeSkill, BuffAttribute):
    def __init__(self):
        level = 2
        buff = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE_BOSS], 2*level)

        AutomateActivativeSkill.__init__(
            self,
            advanced=SkillAdvance.Zero,
            level=level,
            max=2,
            activator= lambda party: CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE], 2*party),
            target=self.Owner
        )
        BuffAttribute.__init__(self,stat=buff)

    def DeleteBuff(self):
        return super().DeleteBuff()

# TODO: 이동 구현. 그 전엔 12%로 가정
class 전투의_흐름(PassiveSkill, BuffAttribute):
    def __init__(self):
        lev = 2
        buff = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE], 6*lev)
        PassiveSkill.__init__(
            self,
            advanced=SkillAdvance.Zero,
            level=lev,
            max=2
        )
        BuffAttribute.__init__(self,stat=buff)

    def DeleteBuff(self):
        return super().DeleteBuff()

# TODO: 공격 상태 구현
class 무아(PassiveSkill, BuffAttribute):
    def __init__(self):
        lev = 2
        buff = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE], 1+5*lev)

        PassiveSkill.__init__(
            self,
            advanced=SkillAdvance.Zero,
            level=lev,
            max=2
        )
        BuffAttribute.__init__(self, stat=buff)

    def DeleteBuff(self):
        return super().DeleteBuff()

class 이네이트_기프트(PassiveSkill, BuffAttribute):
    def __init__(self):
        lev = 2
        buff = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE], 1+2*lev)

        PassiveSkill.__init__(
            self,
            advanced=SkillAdvance.Zero,
            level=lev,
            max=2
        )
        BuffAttribute.__init__(self,stat=buff)

    def DeleteBuff(self):
        return super().DeleteBuff()

class 자신감(PassiveSkill, BuffAttribute):
    def __init__(self):
        lev = 2
        buff = CreateSpecVector([CoreStat.IGNORE_GUARD_PERCENTAGE], 5*lev)

        PassiveSkill.__init__(
            self,
            advanced=SkillAdvance.Zero,
            level=lev,
            max=2
        )
        BuffAttribute.__init__(self,stat=buff)

    def DeleteBuff(self):
        return super().DeleteBuff()
        
class 자연의_벗(PassiveSkill, BuffAttribute):
    def __init__(self):
        lev = 2
        buff = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE], 1 + 2*lev)

        PassiveSkill.__init__(
            self,
            advanced=SkillAdvance.Zero,
            level=lev,
            max=2
        )
        BuffAttribute.__init__(self,stat=buff)

    def DeleteBuff(self):
        return super().DeleteBuff()

class 륀느의_축복(PassiveSkill, BuffAttribute):
    def __init__(self):
        lev = 5
        buff = CreateSpecVector([CoreStat.IGNORE_GUARD_PERCENTAGE], lev*2)
        
        PassiveSkill.__init__(
            self,
            advanced=SkillAdvance.Zero,
            level=lev,
            max=2
        )
        BuffAttribute.__init__(self,stat=buff)

    def DeleteBuff(self):
        return super().DeleteBuff()

class 판단(PassiveSkill, BuffAttribute):
    def __init__(self):
        lev = 2
        buff = CreateSpecVector([CoreStat.CRITICAL_DAMAGE], lev*2)
        
        PassiveSkill.__init__(
            self,
            advanced=SkillAdvance.Zero,
            level=lev,
            max=2
        )
        BuffAttribute.__init__(self,stat=buff)

    def DeleteBuff(self):
        return super().DeleteBuff()
    
    # TODO: deleteBuff 구현해야함

