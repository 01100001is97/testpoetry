from Core.ABCSkill import PassiveSkill, SkillAdvance, OnPressSkill, KeydownSkill, AutomateActivativeSkill
from Core.SpecElements import SpecVector, CoreStat
from Skill.Attributes import *
from Core.Condition import ConditionEnum
from random import random


class 익스트림_매직_썬콜(AutomateActivativeSkill, BuffAttribute):
    def __init__(self, level = 10):
        max = 10
        stat = SpecVector()
        stat[CoreStat.FINAL_DAMAGE_PERCENT] = 2 * level
        
        AutomateActivativeSkill.__init__(
            self=AutomateActivativeSkill, 
            advanced= SkillAdvance.Third,
            level= level,
            max=max,
            # 추후 허수아비 만든 후 람다함수 완성할 것. 
            activator= lambda t: t.GetCondition(),
            target=None
            )
        BuffAttribute.__init__(self=self, stat=stat)


#class 칠링_스텝

class 프로즌_브레이크(AutomateActivativeSkill, BuffAttribute):
    def __init__(self, level = 4):
        max = 4
        stat = SpecVector()
        stat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 2* level

        AutomateActivativeSkill.__init__(
            self=self,
            advanced=SkillAdvance.Third,
            max=max,
            level=level,
            activator=lambda t: t.GetCondition(),
            target=None
        )
        BuffAttribute.__init__(self=self, stat=stat)

# 4차 스킬

class 체인_라이트닝(OnPressSkill, DamageAttribute, DebuffAttribute, BuffAttribute, CombatOrdersAttribute, SkillDelayAttribute):
    def __init__(self, level = 30):
        max = 30
        ChainLighteningIcon = None

        chainlighteningDamage = self.SetChainlighteningDamage(level=level)
        chainlighteningAttackCount = 1
        chainlighteningAttackLine = 10
        
        chainlighteningCondition = [ConditionEnum.스턴]

        chainlighteningStat = SpecVector()
        chainlighteningStat[CoreStat.CRITICAL_PERCENTAGE] = 25

        chainlighteningAttackDelay = Cooldown(milliseconds=780)

        CombatOrdersAttribute

        OnPressSkill.__init__(
            self=self,
            icon=ChainLighteningIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max,
            target=None
            )
        DamageAttribute.__init__(
            self=self, 
            damage_point=chainlighteningDamage, 
            castingCount=chainlighteningAttackCount, 
            line=chainlighteningAttackLine
            )
        DebuffAttribute.__init__(self=self, debuff_stat=SpecVector(), condition=chainlighteningCondition)
        BuffAttribute.__init__(self=self, stat=chainlighteningStat)
        CombatOrdersAttribute.__init__(self=self)
        SkillDelayAttribute.__init__(self=self, casting_delay=chainlighteningAttackDelay)

    # Skill 의 Level getter 재정의
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
        if level > super().MaxLevel:
            level = super().MaxLevel
        
        # 스킬 레벨이 변동되면 스킬의 데미지 또한 그만큼 변경됨
        self._DamagePoint = self.SetChainlighteningDamage(level=level)

    
    def SetChainlighteningDamage(self, level:int):
        """체인 라이트닝의 데미지를 계산함

        Args:
            level (int): 스킬 레벨

        Returns:
            int: 계산된 데미지%
        """
        return 130 + level*3

    def ApplyCombat(self, iscombat: bool):
        self.IsCombat = iscombat
        self.IsApplied = True

        extend = 0
        if self.IsCombat is True:
            extend = 2
        elif self.iscombat is False:
            extend = 1
        else:
            raise AttributeError("IsCombat is None")
        
        self.MaxLevel += extend
        self.Level += extend

    def UseSkill(self, **kwargs):
        return super().UseSkill(**kwargs)

# 명목상 키다운 스킬이지만 단타로 이용되는 특성상 일부 디테일한 묘사는 생략함
class 프리징_브레스(KeydownSkill, DamageAttribute, DebuffAttribute, CombatOrdersAttribute, CooldownAttribute, SkillDelayAttribute):
    def __init__(self, level = 30):
        max = 30
        FreezingBreathIcon = None
        
        # 데미지 및 공격 횟수 설정
        freezingBreathDamage = self.SetFreezingBreathDamage(level=level)
        freezingBreathAttackLine = 3  # 공격 라인(적의 수)
        freezingBreathCastingCount = 1  # 발동 횟수

        # 상태이상 설정
        freezingBreathCondition = [ConditionEnum.바인드]
        # 디버프 스탯 설정
        freezingBreathDebuffStat = SpecVector()
        freezingBreathDebuffStat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 30  # 마법 방어율 30% 감소
        duration = Cooldown(seconds=13)  # 디버프 지속시간
        
        cooldown_time = Cooldown(seconds=180)  # 재사용 대기시간

        # 시전 딜레이
        freezingBreathCastingDelay = Cooldown(milliseconds=960)

        KeydownSkill.__init__(
            self=self,
            icon=FreezingBreathIcon,
            advanced=SkillAdvance.Fourth,  # 가정: 이 스킬은 5차 스킬이라 가정
            level=level,
            max=max,
            # 키다운 지속시간이 스킬의 딜레이와 동일(적용 후 키다운 해제)
            keydowntime=freezingBreathCastingDelay,
            target=None
            )
        DamageAttribute.__init__(
            self=self, 
            damage_point=freezingBreathDamage, 
            castingCount=freezingBreathCastingCount, 
            line=freezingBreathAttackLine
            )
        DebuffAttribute.__init__(self=self, debuff_stat=freezingBreathDebuffStat, condition=freezingBreathCondition)
        CombatOrdersAttribute.__init__(self=self)
        CooldownAttribute.__init__(self=self, cooldown=cooldown_time, isresetable=True)
        SkillDelayAttribute.__init__(self, casting_delay=freezingBreathCastingDelay)

 
       # Skill 의 Level getter 재정의
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
        if level > super().MaxLevel:
            level = super().MaxLevel
        
        # 스킬 레벨이 변동되면 스킬의 데미지 또한 그만큼 변경됨
        self.DOTDamagePoint = self.SetFreezingBreathDamage(level=level)

    
    def SetFreezingBreathDamage(self, level:int):
        """프리징 브레스의 데미지를 계산함

        Args:
            level (int): 스킬 레벨

        Returns:
            int: 계산된 데미지%
        """
        return 50 + level

    def ApplyCombat(self, iscombat: bool):
        self.IsCombat = iscombat
        self.IsApplied = True

        extend = 0
        if self.IsCombat is True:
            extend = 2
        elif self.iscombat is False:
            extend = 1
        else:
            raise AttributeError("IsCombat is None")
        
        self.MaxLevel += extend
        self.Level += extend

    def UseSkill(self, **kwargs):
        return super().UseSkill(**kwargs)

class 블리자드(OnPressSkill, DamageAttribute, CooldownAttribute, SkillDelayAttribute, CombatOrdersAttribute, DebuffAttribute):
    def __init__(self, level = 30):
        max = 30
        BlizzardIcon = None
        
        blizzardDamage = self.SetBlizzardDamage(level=level)
        blizzardAttackLine = 12  # 공격 라인(적의 수)
        blizzardCastingCount = 1  # 발동 횟수

        blizzardCooldown = Cooldown(seconds=45)  # 재사용 대기시간

        blizzardCastingDelay = Cooldown(milliseconds=900)

        blizzardCondition = [ConditionEnum.빙결]

        OnPressSkill.__init__(
            self=self,
            icon=BlizzardIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max,
            target=None
            )
        DamageAttribute.__init__(
            self=self, 
            damage_point=blizzardDamage, 
            castingCount=blizzardCastingCount, 
            line=blizzardAttackLine
            )
        CooldownAttribute.__init__(self=self, cooldown=blizzardCooldown, isresetable=True)
        SkillDelayAttribute.__init__(self=self, casting_delay=blizzardCastingDelay)
        CombatOrdersAttribute.__init__(self=self)
        DebuffAttribute.__init__(self=self, debuff_stat=SpecVector(), condition=blizzardCondition)

    def SetBlizzardDamage(self, level:int):
        """블리자드의 데미지를 계산함

        Args:
            level (int): 스킬 레벨

        Returns:
            int: 계산된 데미지%
        """
        return 211 + 3 * level

    @property
    def Level(self):
        return super().Level
    
    @Level.setter
    def Level(self, level:int):
        if not isinstance(level, int) or level < 0:
            raise ValueError("Level must be a non-negative integer")
        if level > super().MaxLevel:
            level = super().MaxLevel
        
        self.DOTDamagePoint = self.SetBlizzardFinalAttackDamage(level=level)


    def ApplyCombat(self, iscombat: bool):
        self.IsCombat = iscombat
        self.IsApplied = True

        extend = 0
        if self.IsCombat is True:
            extend = 2
        elif self.iscombat is False:
            extend = 1
        else:
            raise AttributeError("IsCombat is None")
        
        self.MaxLevel += extend
        self.Level += extend

    def UseSkill(self, **kwargs):
        return super().UseSkill(**kwargs)

class 블리자드_파이널어택(AutomateActivativeSkill, DamageAttribute, CombatOrdersAttribute, DebuffAttribute):
    def __init__(self, level = 30):
        max = 30
        
        blizzardFinalAttackDamage = self.SetBlizzardFinalAttackDamage(level=level)
        blizzardFinalAttackLine = 1  # 공격 라인(적의 수)
        blizzardFinalAttackCastingCount = 1  # 발동 횟수

        AutomateActivativeSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max,
            target=None,
            activator=lambda skilllevel: random.choices([True, False], weights=[2 * skilllevel, 100 - 2 * skilllevel])[0]
            )
        DamageAttribute.__init__(
            self=self, 
            damage_point=blizzardFinalAttackDamage, 
            castingCount=blizzardFinalAttackCastingCount, 
            line=blizzardFinalAttackLine
            )
        CombatOrdersAttribute.__init__(self=self)
        DebuffAttribute.__init__(self=self, condition=[ConditionEnum.빙결], debuff_stat=SpecVector())

    def SetBlizzardFinalAttackDamage(self, level:int):
        """블리자드 파이널 어택의 데미지를 계산함

        Args:
            level (int): 스킬 레벨

        Returns:
            int: 계산된 데미지%
        """
        return 100 + 4 * level

    # CombatOrdersAttribute 및 Level의 setter, ApplyCombat 메서드는 이전과 동일

    @property
    def Level(self):
        return super().Level
    
    @Level.setter
    def Level(self, level:int):
        if not isinstance(level, int) or level < 0:
            raise ValueError("Level must be a non-negative integer")
        if level > super().MaxLevel:
            level = super().MaxLevel
        
        self.DOTDamagePoint = self.SetBlizzardFinalAttackDamage(level=level)

    def ApplyCombat(self, iscombat: bool):
        self.IsCombat = iscombat
        self.IsApplied = True

        extend = 0
        if self.IsCombat is True:
            extend = 2
        elif self.iscombat is False:
            extend = 1
        else:
            raise AttributeError("IsCombat is None")
        
        self.MaxLevel += extend
        self.Level += extend


class 프로즌_오브(OnPressSkill, DamageAttribute, DebuffAttribute, DurationAttribute, IntervalAttribute, CooldownAttribute, SkillDelayAttribute, CombatOrdersAttribute):
    def __init__(self, level = 30):
        max = 30
        FrozenOrbIcon = None

        frozenOrbDamage = self.SetFrozenOrbDamage(level=level)
        frozenOrbAttackLine = 1  # 공격 라인(적의 수)
        frozenOrbCastingCount = 1  # 발동 횟수

        frozenOrbCooldown = Cooldown(seconds=5)  # 재사용 대기시간

        frozenOrbCastingDelay = Cooldown(milliseconds=900)

        frozenOrbCondition = [ConditionEnum.빙결]

        frozenOrbDuration = Cooldown(seconds=4)

        frozenOrbInterval = Cooldown(milliseconds=210)

        OnPressSkill.__init__(
            self=self,
            icon=FrozenOrbIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max,
            target=None
            )
        DamageAttribute.__init__(
            self=self, 
            damage_point=frozenOrbDamage, 
            castingCount=frozenOrbCastingCount, 
            line=frozenOrbAttackLine
            )
        DebuffAttribute.__init__(self=self, debuff_stat=SpecVector(), condition=frozenOrbCondition)
        DurationAttribute.__init__(self=self, duration=frozenOrbDuration, serverlack=False, isbuffmult=False)
        IntervalAttribute.__init__(self=self, interval=frozenOrbInterval)
        CooldownAttribute.__init__(self=self, cooldown=frozenOrbCooldown, isresetable=True)
        SkillDelayAttribute.__init__(self=self, casting_delay=frozenOrbCastingDelay)
        CombatOrdersAttribute.__init__(self=self)

    def SetFrozenOrbDamage(self, level:int) -> int:
        """
        스킬 레벨에 따른 프로즌 오브의 데미지를 계산하는 메서드입니다.

        Args:
            level (int): 스킬의 레벨

        Returns:
            int: 계산된 프로즌 오브의 데미지
        """
        return 100+4*level

    @property
    def Level(self):
        return super().Level
    
    @Level.setter
    def Level(self, level:int):
        if not isinstance(level, int) or level < 0:
            raise ValueError("Level must be a non-negative integer")
        if level > super().MaxLevel:
            level = super().MaxLevel
        
        self.DOTDamagePoint = self.SetBlizzardFinalAttackDamage(level=level)

    def ApplyCombat(self, iscombat: bool):
        self.IsCombat = iscombat
        self.IsApplied = True

        extend = 0
        if self.IsCombat is True:
            extend = 2
        elif self.iscombat is False:
            extend = 1
        else:
            raise AttributeError("IsCombat is None")
        
        self.MaxLevel += extend
        self.Level += extend

    def UseSkill(self, **kwargs):
        return super().UseSkill(**kwargs)