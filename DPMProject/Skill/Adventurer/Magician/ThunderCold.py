from Core.ABCSkill import PassiveSkill, SkillAdvance, OnPressSkill, KeydownSkill, AutomateActivativeSkill
from Core.SpecElements import SpecVector, CoreStat, CreateSpecVector
from Skill.Attributes import *
from Core.Condition import ConditionEnum
from Core.Probability import SuccessProbability
from random import random
from Character.ABCCharacter import ABCCharacter
from Dummy.Dummy import Dummy
from datetime import timedelta
import random

class ThunderColdDamageAttribute(DamageAttribute):
    """썬콜 스킬 중 프로스트 이펙ㅌ, 익스트림 매직을 선반영한 속성

    Args:
        DamageAttribute (_type_): _description_
    """
    def __init__(self, damage_point: int, line: int, castingCount: int = 1):
        super().__init__(damage_point, line, castingCount)
        #.__init__(self, icon, advanced= advanced, level=level , max=max)

    def GetColdStack(self):
        """현재 빙결스택을 반환함

        Raises:
            AttributeError: _description_

        Returns:
            _type_: _description_
        """
        if self.Target == None or self.Owner == None:
            raise AttributeError("Target, Owner이 아직 셋팅되지 않았음")
        
        coldstack = self.Target._Condition[ConditionEnum.빙결]
        if coldstack > 5 or coldstack < 0:
            raise("ColdStack 은 0~5중첩 가능함")
        
        return coldstack
    
    def ColdAttackBuff(self):
        """얼음 속성 공격 시 얻는 버프 효과 반환
        """
        coldStack = self.GetColdStack()
        buffStat = SpecVector()
        buffStat[CoreStat.IGNORE_GUARD_PERCENTAGE] = coldStack * 2
        buffStat[CoreStat.DAMAGE_PERCENTAGE] = 12 * coldStack
        
        
        if coldStack + self.Target._Condition[ConditionEnum.스턴] > 0:
            buffStat[CoreStat.FINAL_DAMAGE_PERCENT] = 20

        self.IncrementCold()
        return buffStat

    def IncrementCold(self):
        self.Target.increment_condition(ConditionEnum.빙결)

    def DecrementCold(self):
        self.Target.decrement_condition(ConditionEnum.빙결)
    def ThunderAttackBuff(self):
        """번개 속성 공격 시 얻는 버프 효과 반환

        Returns:
            _type_: _description_
        """
        coldStack = self.GetColdStack()
        # ColdAttackBuff 에서 빙결스택을 올려주므로 다시 내려줌
        stat = self.ColdAttackBuff()
        self.DecrementCold()

        stat[CoreStat.CRITICAL_DAMAGE] = 3 * coldStack

        #번개 공격 시 빙결 중첩 -1 단, 썬더스피어는 빙결 스택을 감소시키지 않음
        if issubclass(type(self),썬더_스피어):
            pass
        else:
            self.DecrementCold()

        return stat

    def UseFinalAttack(self):
        """공격 시 파이널어택(블리자드) 발동
        """
        Blizzard = self._FinalAttack()
        Blizzard.Target = self.Target
        Blizzard.Owner = self.Owner
        Blizzard.ApplyCombat(iscombat = self.IsCombat)
        if Blizzard.Activator(Blizzard.Level):
            return Blizzard.UseSkill()
      
        


# 3차 스킬
class 썬더_스피어:
    pass

# 4차 스킬

class 체인_라이트닝(OnPressSkill, ThunderColdDamageAttribute, DebuffAttribute, BuffAttribute, CombatOrdersAttribute, SkillDelayAttribute, FinalAttackAttribute):
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

        finalAttackName = 블리자드_파이널어택
        
        OnPressSkill.__init__(
            self=self,
            icon=ChainLighteningIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max
            )
        ThunderColdDamageAttribute.__init__(
            self=self, 
            damage_point=chainlighteningDamage, 
            castingCount=chainlighteningAttackCount, 
            line=chainlighteningAttackLine
            )
        DebuffAttribute.__init__(self=self, debuff_stat=SpecVector(), condition=chainlighteningCondition)
        BuffAttribute.__init__(self=self, stat=chainlighteningStat)
        CombatOrdersAttribute.__init__(self=self)
        SkillDelayAttribute.__init__(self=self, casting_delay=chainlighteningAttackDelay)
        FinalAttackAttribute.__init__(self=self, finalAttack=finalAttackName)

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

    def ApplyCombat(self, isOriginal: bool):
        """스킬에 컴뱃 오더스 효과를 적용시킴

        Args:
            isOriginal (bool): True: 찐컴뱃, False: 쓸컴뱃

        Raises:
            AttributeError: _description_
            AttributeError: _description_
        """
        if isOriginal == None:
            raise AttributeError("컴뱃 오더스 펫버프에서 누락됨")
        self.IsCombat = isOriginal
        self.IsApplied = True

        extend = 0
        if self.IsCombat is True:
            extend = 2
        elif self.IsCombat is False:
            extend = 1
        else:
            raise AttributeError("IsCombat is None")
        
        self.MaxLevel += extend
        self.Level += extend

    def UseSkill(self):
        """체인 라이트닝을 사용함

        Args:
            time (timedelta): _description_

        Raises:
            TypeError: _description_
            TypeError: _description_

        Returns:
            _type_: _description_
        """
        if not isinstance(self.Owner, ABCCharacter):
            raise TypeError("스킬의 소유자가 설정되지 않앗음")
        
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        
        # 체인 라이트닝의 상태이상 효과 추가함
        self.Target.Condition[ConditionEnum.스턴] = 1
        self.Done = True
        
        # 번개 속성 공격 시 빙결스택에 따른 버프 효과를 받아옴
        buff = self.BuffStat
        buff += self.ThunderAttackBuff()

        # 데미지를 계산
        chainLighteningLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = buff)

        # 데미지가 유효하면 파이널어택을 발동시킴
        blizzardFinalLog = None
        if chainLighteningLog is not None:
            blizzardFinalLog = self.UseFinalAttack()

        return [chainLighteningLog, blizzardFinalLog]
        # 속성 부여 등등

    def DeleteDebuff(self):
        """버프 사라질 때 호출
        """
        self.Target._Condition[ConditionEnum.스턴] -= 1

    def DeleteBuff(self):
        pass    

    def __del__(self):
        self.DeleteBuff()
        self.DeleteDebuff()



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
            max=max
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
        
        self.DamagePoint = self.SetBlizzardFinalAttackDamage(level=level)

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
        self.DamagePoint = self.SetFreezingBreathDamage(level=level)

    
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
            max=max
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
        
        self.DamagePoint = self.SetBlizzardFinalAttackDamage(level=level)


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

class 블리자드_파이널어택(AutomateActivativeSkill,ThunderColdDamageAttribute, CombatOrdersAttribute, DebuffAttribute):
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
            activator=lambda skilllevel: SuccessProbability(2*skilllevel)
            )
        ThunderColdDamageAttribute.__init__(
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
        
        self.DamagePoint = self.SetBlizzardFinalAttackDamage(level=level)

    def DeleteDebuff(self):
        pass

    def UseSkill(self):
        # 번개 속성 공격 시 빙결스택에 따른 버프 효과를 받아옴
        buff = self.ColdAttackBuff()

        # TODO: 파이널 어택 공격 시 버프 효과 적용(푸소, 피에르)
    
        # 데미지를 계산
        log = self.Target.TakeAttack(char=self.Owner, skill=self, add = buff)

        return log
