from Core.ABCSkill import PassiveSkill, SkillAdvance, OnPressSkill, KeydownSkill, AutomateActivativeSkill, OriginSkill
from Core.SpecElements import SpecVector, CoreStat, CreateSpecVector
from Skill.Attributes import *
from Skill.CommonSkill import 스파이더_인_미러, 스파이더_인_미러_거울속의_거미, 크레스트_오브_더_솔라, 크레스트_오브_더_솔라_불꽃의_문양
from Core.Condition import ConditionEnum
from Core.Probability import SuccessProbability
from random import random
from Character.ABCCharacter import ABCCharacter
from Dummy.Dummy import Dummy, DummySize
from datetime import timedelta
import random
import math

class ThunderColdDamageAttribute(DamageAttribute):
    """썬콜 스킬 중 프로스트 이펙ㅌ, 익스트림 매직을 선반영한 속성

    Args:
        DamageAttribute (_type_): _description_
    """
    def __init__(self, damage_point: int, line: int, castingCount: int = 1):
        super().__init__(damage_point, line, castingCount)
        #.__init__(self, icon, advanced= advanced, level=level , max=max)

    def _GetColdStack(self):
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
        coldStack = self._GetColdStack()
        buffStat = SpecVector()
        buffStat[CoreStat.IGNORE_GUARD_PERCENTAGE] = coldStack * 2
        
        buffStat[CoreStat.CRITICAL_DAMAGE] = 3 * coldStack
        
        if coldStack + self.Target._Condition[ConditionEnum.스턴] > 0:
            buffStat[CoreStat.FINAL_DAMAGE_PERCENT] = 20

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
        coldStack = self._GetColdStack()
        # ColdAttackBuff 에서 빙결스택을 올려주므로 다시 내려줌
        stat = self.ColdAttackBuff()
        stat[CoreStat.DAMAGE_PERCENTAGE] = 12 * coldStack
        

        return stat

    def UseFinalAttack(self):
        """공격 시 파이널어택(블리자드) 발동
        """
        Blizzard = self._FinalAttack()
        Blizzard.Target = self.Target
        Blizzard.Owner = self.Owner
        Blizzard.ApplyCombat(isOriginal= False)
        
        return Blizzard.UseSkill()
      
# 3차 스킬
class 썬더_스피어(OnPressSkill, ThunderColdDamageAttribute, SummonAttribute, SkillDelayAttribute):
    def __init__(self, level = 20):
        max = 20
        ThunderSpearIcon = None

        ThunderSpearDamage = self.SetThunderSpearDamage(level=level)
      
        ThunderSpearDamageLine = 3

        ThunderSpearAttackDelay = Cooldown(milliseconds=900)
        ThunderSpearInterval = Cooldown(milliseconds=1080)
        ThunderSpearDuration = Cooldown(seconds=120)

        OnPressSkill.__init__(
            self=self,
            icon=ThunderSpearIcon,
            advanced=SkillAdvance.Third,
            level=level,
            max=max
        )
        ThunderColdDamageAttribute.__init__(
            self=self,
            damage_point=ThunderSpearDamage,
            line=ThunderSpearDamageLine
        )
        SummonAttribute.__init__(
            self=self,
            duration=ThunderSpearDuration,
            interval=ThunderSpearInterval,
            mult=True
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=ThunderSpearAttackDelay,
            applyAttackSpeed=False
        )

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
        if level > self.MaxLevel:
            self._level = level
        self._level = level
        
        # 스킬 레벨이 변동되면 스킬의 데미지 또한 그만큼 변경됨
        self._DamagePoint = self.SetChainlighteningDamage(level=level)

    def SetThunderSpearDamage(self, level:int):
        return 250+6*level
    
    def UseSkill(self):
        if not isinstance(self.Owner, ABCCharacter):
            raise TypeError("스킬의 소유자가 설정되지 않앗음")
        
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        
        
        buff = self.ThunderAttackBuff()
        # 썬더스피어는 빙결 스택을 감소시키지 않음

        if 썬더_스피어_강화_5th in self.Owner._PassiveSkillList:
            buff += 썬더_스피어_강화_5th().ThunderSpaerCoreReinforce

        # 데미지 계산
        ThunderspearLog = self.Target.TakeAttack(
            char=self.Owner,
            skill=self,
            add=buff
        )

        return [ThunderspearLog]

class 썬더_스피어_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        self.ThunderSpaerCoreReinforce = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level * 썬더_스피어().Advanced.value)
        self.ThunderSpaerCoreReinforce[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20
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
        SkillDelayAttribute.__init__(self=self, casting_delay=chainlighteningAttackDelay, applyAttackSpeed=True)
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
        if level > self.MaxLevel:
            self._level = level
        self._level = level
        
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
        
        
        # 번개 속성 공격 시 빙결스택에 따른 버프 효과를 받아옴
        buff = self._BuffStat
        buff += self.ThunderAttackBuff()
        self.DecrementCold()

        if 체인_라이트닝_강화_6th in self.Owner._PassiveSkillList:
            upgrade = 체인_라이트닝_강화_6th()
            self.DamagePoint = upgrade.ChainLightening6thDamage
            self.BuffStat += upgrade.ChainLightening6thCrit
            

        if 체인_라이트닝_강화_5th in self.Owner._PassiveSkillList:
            buff += 체인_라이트닝_강화_5th().ChainCoreReinforce

        if 체인_라이트닝_리인포스 in self.Owner._PassiveSkillList:
            buff += 체인_라이트닝_리인포스().ChainReinforce

        if 체인_라이트닝_보너스어택 in self.Owner._PassiveSkillList:
            self.AttackLine += 체인_라이트닝_보너스어택().ChainAddAttackLine

        # 데미지를 계산
        chainLighteningLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = buff)


        # 데미지가 유효하면 파이널어택을 발동시킴
        blizzardFinalLog = None
        if chainLighteningLog is not None:
            
            blizzardFinalLog = self.UseFinalAttack()

        if 체인_라이트닝_강화_6th in self.Owner._PassiveSkillList:
            summon = 체인_라이트닝_전류지대()
            if summon.NumOfSummoned <= summon.MaxStack:
                
                summon.Owner = self.Owner
                summon.Target = self.Target
                # 7초마다 소환
                if self.Owner.CooldownManager.isReady(체인_라이트닝_전류지대):
                    self.Owner.CooldownManager.Count(체인_라이트닝_전류지대)
                    summon.NumOfSummoned += 1
                    self.Owner.SummonManager.Add(summon)
                else:
                    # 일정 확률로 소환
                    if (random.random() < 체인_라이트닝_전류지대().fieldProb/100):
                        summon.NumOfSummoned += 1
                        self.Owner.SummonManager.Add(summon)
      
        self.Done = True
        return [chainLighteningLog, blizzardFinalLog]

class 체인_라이트닝_리인포스(PassiveSkill):
    def __init__(self):
        self.ChainReinforce = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE], 20)

class 체인_라이트닝_보너스어택(PassiveSkill):
    def __init__(self):
        self.ChainAddAttackLine = 1

class 체인_라이트닝_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        self.ChainCoreReinforce = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level * 체인_라이트닝().Advanced.value)
        self.ChainCoreReinforce[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20

class 체인_라이트닝_강화_6th(PassiveSkill):
    def __init__(self, level=30):
        max = 30
        self.ChainLightening6thDamage = 305
        self.ChainLightening6thCrit = CreateSpecVector([CoreStat.CRITICAL_PERCENTAGE], 5)

        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Sixth,
            level=level,
            max=max
        )
        
        
        
class 체인_라이트닝_전류지대(OnPressSkill, SummonAttribute, ThunderColdDamageAttribute, StackAttribute, SkillDelayAttribute, CooldownAttribute):
    NumOfSummoned:int

    def __new__(cls):
        cls.NumOfSummoned = 0
        return super().__new__(cls)

    def __init__(self, level=체인_라이트닝_강화_6th().Level):
        max = 체인_라이트닝_강화_6th().MaxLevel
        
        fieldDuration = Cooldown(seconds=4)
        fieldInterval = Cooldown(milliseconds=750)
        fieldCooldown = Cooldown(seconds=7)
        fieldDamage = 140
        fieldDamageLine = 2
        self.fieldProb = 35
        

        
        OnPressSkill.__init__(
            self=self,
            icon=체인_라이트닝().Icon,
            advanced=SkillAdvance.Sixth,
            level=level,
            max=max
        )
        SummonAttribute.__init__(
            self=self,
            duration=fieldDuration,
            interval=fieldInterval,
            mult=False
        )
        ThunderColdDamageAttribute.__init__(
            self=self,
            damage_point=fieldDamage,
            line=fieldDamageLine
        )
        StackAttribute.__init__(
            self=self,
            max_stack=4,
            charged_stack=0,
            charge_cooltime=0
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=fieldCooldown,
            isresetable=False
        )

    def UseSkill(self):
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        
        
        buff = self.ThunderAttackBuff()
        if self.ChargedStack == 0:
            self.DecrementCold()
        elif self.ChargedStack == 3:
            self.EndSummon()
            del self
            return []

        
        fieldLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = buff)
        
        
        self.ChargedStack += 1

        return [fieldLog]
    
    def EndSummon(self):
        self.NumOfSummoned -= 1
   

class 프로즌_오브(OnPressSkill, ThunderColdDamageAttribute, SummonAttribute, CooldownAttribute, SkillDelayAttribute, CombatOrdersAttribute, FinalAttackAttribute):
    def __init__(self, level = 30):
        max = 30
        FrozenOrbIcon = None

        frozenOrbDamage = self.SetFrozenOrbDamage(level=level)
        frozenOrbAttackLine = 1  # 공격 라인(적의 수)
        frozenOrbCastingCount = 1  # 발동 횟수

        frozenOrbCooldown = Cooldown(seconds=5)  # 재사용 대기시간

        frozenOrbCastingDelay = Cooldown(milliseconds=900)

        frozenOrbDuration = Cooldown(seconds=4)

        frozenOrbInterval = Cooldown(milliseconds=210)

        OnPressSkill.__init__(
            self=self,
            icon=FrozenOrbIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max
            )
        ThunderColdDamageAttribute.__init__(
            self=self, 
            damage_point=frozenOrbDamage, 
            castingCount=frozenOrbCastingCount, 
            line=frozenOrbAttackLine
            )
        SummonAttribute.__init__(self, duration=frozenOrbDuration, interval=frozenOrbInterval, mult=False)
        CooldownAttribute.__init__(self=self, cooldown=frozenOrbCooldown, isresetable=True)
        SkillDelayAttribute.__init__(self=self, casting_delay=frozenOrbCastingDelay, applyAttackSpeed=True)
        CombatOrdersAttribute.__init__(self=self)
        FinalAttackAttribute.__init__(self, finalAttack=블리자드_파이널어택)

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
        if level > self.MaxLevel:
            self._level = level
        self._level = level
        
        self.DamagePoint = self.SetFrozenOrbDamage(level=level)

    def UseSkill(self):
        if not isinstance(self.Owner, ABCCharacter):
            raise TypeError("스킬의 소유자가 설정되지 않앗음")
        
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        
        buff = self.ColdAttackBuff()
        self.IncrementCold()

        if 프로즌_오브_강화_5th in self.Owner._PassiveSkillList:
            buff += 프로즌_오브_강화_5th().FrozenCoreReinforce

        if 프로즌_오브_리인포스 in self.Owner._PassiveSkillList:
            buff += 프로즌_오브_리인포스().FrozenReinforce
        
        frozenOrbLog = self.Target.TakeAttack(char=self.Owner, skill=self, add=buff)
        
        blizzardFinalLog = None
        if frozenOrbLog is not None:
            # 빙결 중첩
            
            # 파이널 어택 발동
            blizzardFinalLog = self.UseFinalAttack()

        return [frozenOrbLog, blizzardFinalLog]

class 프로즌_오브_리인포스(PassiveSkill):
    def __init__(self):
        self.FrozenReinforce = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE], 20)

class 프로즌_오브_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        self.FrozenCoreReinforce = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level * 프로즌_오브().Advanced.value)
        self.FrozenCoreReinforce[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20


# 명목상 키다운 스킬이지만 단타로 이용되는 특성상 일부 디테일한 묘사는 생략함
class 프리징_브레스(OnPressSkill, ThunderColdDamageAttribute, DebuffAttribute, CombatOrdersAttribute, CooldownAttribute, SkillDelayAttribute, DurationAttribute, FinalAttackAttribute):
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

        finalAttack = 블리자드_파이널어택

        OnPressSkill.__init__(
            self=self,
            icon=FreezingBreathIcon,
            advanced=SkillAdvance.Fourth,  # 가정: 이 스킬은 5차 스킬이라 가정
            level=level,
            max=max,
            # 키다운 지속시간이 스킬의 딜레이와 동일(적용 후 키다운 해제)
            )
        ThunderColdDamageAttribute.__init__(
            self=self, 
            damage_point=freezingBreathDamage, 
            castingCount=freezingBreathCastingCount, 
            line=freezingBreathAttackLine
            )
        DebuffAttribute.__init__(self=self, debuff_stat=freezingBreathDebuffStat, condition=freezingBreathCondition)
        CombatOrdersAttribute.__init__(self=self)
        CooldownAttribute.__init__(self=self, cooldown=cooldown_time, isresetable=True)
        SkillDelayAttribute.__init__(self, casting_delay=freezingBreathCastingDelay, applyAttackSpeed=True)
        DurationAttribute.__init__(
            self=self,
            duration=duration,
            serverlack=False,
            isbuffmult=False
        )
        FinalAttackAttribute.__init__(self, finalAttack=finalAttack)
 
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
        if level > self.MaxLevel:
            self._level = level
        self._level = level
        
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


    def UseSkill(self, **kwargs):
        if not isinstance(self.Owner, ABCCharacter):
            raise TypeError("스킬의 소유자가 설정되지 않앗음")
        
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        
        
        buff = self.ColdAttackBuff()
        self.IncrementCold()
        self.Target._DebuffManager.Add(self)

        FreezingBreathLog = self.Target.TakeAttack(
            char=self.Owner,
            skill=self,
            add=buff
        )
        blizzardFinalLog = None
        if FreezingBreathLog is not None:
            # 빙결 중첩
            
            # 파이널 어택 발동
            blizzardFinalLog = self.UseFinalAttack()

        return [FreezingBreathLog, blizzardFinalLog]

class 블리자드(OnPressSkill, ThunderColdDamageAttribute, CooldownAttribute, SkillDelayAttribute, CombatOrdersAttribute):
    def __init__(self, level = 30):
        max = 30
        BlizzardIcon = None
        
        blizzardDamage = self.SetBlizzardDamage(level=level)
        blizzardAttackLine = 12  # 공격 라인(적의 수)
        blizzardCastingCount = 1  # 발동 횟수

        blizzardCooldown = Cooldown(seconds=45)  # 재사용 대기시간

        blizzardCastingDelay = Cooldown(milliseconds=900)

        OnPressSkill.__init__(
            self=self,
            icon=BlizzardIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max
            )
        ThunderColdDamageAttribute.__init__(
            self=self,
            damage_point=blizzardDamage, 
            castingCount=blizzardCastingCount, 
            line=blizzardAttackLine
            )
        CooldownAttribute.__init__(self=self, cooldown=blizzardCooldown, isresetable=True)
        SkillDelayAttribute.__init__(self=self, casting_delay=blizzardCastingDelay, applyAttackSpeed=True)
        CombatOrdersAttribute.__init__(self=self)
        

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
        if level > self.MaxLevel:
            self._level = level
        self._level = level
        
        self.DamagePoint = self.SetBlizzardDamage(level=level)


    def UseSkill(self, **kwargs):
        if not isinstance(self.Owner, ABCCharacter):
            raise TypeError("스킬의 소유자가 설정되지 않앗음")
        
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        
        if 블리자드_강화_5th in self.Owner._PassiveSkillList:
            buff += 블리자드_강화_5th().blizzardCoreReinforce

        
        buff = self.ColdAttackBuff()
        self.IncrementCold()

        BlizzardDamageLog = self.Target.TakeAttack(
            char=self.Owner,
            skill=self,
            add=buff
        )
        return [BlizzardDamageLog]

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
            max=max
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
        if level > self.MaxLevel:
            self._level = level
        self._level = level
        
        self.DamagePoint = self.SetBlizzardFinalAttackDamage(level=level)

    @classmethod
    def active(self):
        return False

    def UseSkill(self):
        
        # TODO: 파이널 어택 공격 시 버프 효과 적용(푸소, 피에르)
    
        # 확률에 따라 발동함
        log = None
        if (lambda: True if random.random() <= 0.01*self.Level*2 else False)():

            # 번개 속성 공격 시 빙결스택에 따른 버프 효과를 받아옴
            buff = self.ColdAttackBuff()
            self.IncrementCold()
             
            if 블리자드_강화_5th in self.Owner._PassiveSkillList:
                buff += 블리자드_강화_5th().blizzardCoreReinforce

        # 데미지를 계산
            log = self.Target.TakeAttack(char=self.Owner, skill=self, add = buff)
        return log

class 블리자드_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        self.blizzardCoreReinforce = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level * 블리자드().Advanced.value)
        self.blizzardCoreReinforce[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20

class 엘퀴네스(OnPressSkill, ThunderColdDamageAttribute, SummonAttribute, SkillDelayAttribute, CombatOrdersAttribute, MasteryAttribute, FinalAttackAttribute):
    def __init__(self, level = 30):
        max = 30
        elquinessIcon = None
        elquinessDamage = self.SetElquinessDamage(level = level)
        elquinessDamageLine = 3
        elquinessSummonDelay = Cooldown(milliseconds=600)
        elquinessInterval = Cooldown(milliseconds=3000)
        elquinessDuration = Cooldown(seconds=self.SetElquinessDuration(level=level))

        OnPressSkill.__init__(
            self=self,
            icon=elquinessIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max
        )
        ThunderColdDamageAttribute.__init__(
            self=self,
            damage_point=elquinessDamage,
            line=elquinessDamageLine
        )
        SummonAttribute.__init__(
            self=self,
            duration=elquinessDuration,
            interval=elquinessInterval,
            mult=True
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=elquinessSummonDelay,
            applyAttackSpeed=False
        )
        CombatOrdersAttribute.__init__(self)
        MasteryAttribute.__init__(self, mastery=self.SetElquinessMastery(level=level))
        FinalAttackAttribute.__init__(self, finalAttack=블리자드_파이널어택)


    def SetElquinessMastery(self, level:int):
        return 55 + round(level/2)

    def SetElquinessDuration(self, level:int):
        return 100+5*level

    def SetElquinessDamage(self, level:int):
        return 67 + 2*level
    
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
        
        self._DamagePoint = self.SetElquinessDamage(level=level)
        self._Mastery = self.SetElquinessMastery(level=level)
        self._Duration =Cooldown(seconds=self.SetElquinessDuration(level=level))

    def UseSkill(self):
        if not isinstance(self.Owner, ABCCharacter):
            raise TypeError("스킬의 소유자가 설정되지 않앗음")
        
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
    
        buff = self.ColdAttackBuff()

         
        if 엘퀴네스_강화_5th in self.Owner._PassiveSkillList:
            buff += 엘퀴네스_강화_5th().ElquinessCoreReinforce


        ElquinessLog = self.Target.TakeAttack(
            char=self.Owner,
            skill=self,
            add=buff
        )

        # 데미지가 유효하면 파이널어택을 발동시킴
        blizzardFinalLog = None
        if ElquinessLog is not None:
            
            blizzardFinalLog = self.UseFinalAttack()

        
        return [ElquinessLog, blizzardFinalLog]
    
class 엘퀴네스_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        self.ElquinessCoreReinforce = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level * 엘퀴네스().Advanced.value)
        self.ElquinessCoreReinforce[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20

class 인피니티(OnPressSkill, BuffAttribute, StackAttribute, CombatOrdersAttribute, CooldownAttribute, DurationAttribute, SkillDelayAttribute):
    def __init__(self, level=30):
        max=30
        infiniteIcon =None
        infiniteDuration = self.GetInfinityDuration(level)
        infiniteStat = lambda: None
        infiniteCooldown = Cooldown(seconds=180)
        infiniteDelay = Cooldown(milliseconds=600)
        
        OnPressSkill.__init__(
            self,
            icon=infiniteIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max
        )
        BuffAttribute.__init__(
            self=self,
            stat=infiniteStat
        )
        StackAttribute.__init__(
            self=self,
            max_stack= 0,
            charged_stack= 0,
            charge_cooltime= 5
        )
        CombatOrdersAttribute.__init__(self)
        CooldownAttribute.__init__(self=self, cooldown=infiniteCooldown, isresetable=False)
        DurationAttribute.__init__(self=self, duration=infiniteDuration, serverlack=True, isbuffmult=True)
        SkillDelayAttribute.__init__(self=self, casting_delay=infiniteDelay, applyAttackSpeed=True, special=False)

    def GetInfiniteStat(self, level:int):
        return lambda passedTime:  CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT],min(115,40+ level + math.ceil(passedTime.total_seconds() / 5)* 3))

    def GetInfinityDuration(self,level:int):
        return Cooldown(seconds=level + 10)
    
    def GetMaxStack(self, level:int):
        return math.ceil(self.Duration.total_seconds() * (1 + self.Owner._BuffDuration/100)/5)
    
    @property
    def Level(self):
        return super().Level
    
    @Level.setter
    def Level(self, level:int):
        if not isinstance(level, int) or level < 0:
            raise ValueError("Level must be a non-negative integer")
        if level > self.MaxLevel:
            self._level = level
        self._level = level

        self._BuffStat = self.GetInfiniteStat(level=level)
        self.Duration = self.GetInfinityDuration(level=level)
        self.MaxStack = self.GetMaxStack(level=level)


    def UseSkill(self):
        if not isinstance(self.Owner, ABCCharacter):
            raise TypeError("스킬의 소유자가 설정되지 않앗음")
        
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        
    
    @property
    def BuffStat(self):
        return self.GetInfiniteStat(level=self.Level)

class 라이트닝_스피어(KeydownSkill, ThunderColdDamageAttribute, CooldownAttribute, DurationAttribute, SkillDelayAttribute, IntervalAttribute, FinalAttackAttribute):

    def __init__(self, level =1):
        max = 1
        lighteningSpearIcon = None
        lighteningSpearDamage = self.SetChainLighteningDamage()
        lighteningSpearAttackLine = 15
        lighteningSpearAttackCount = 4
        lighteningSpearCooldown = Cooldown(seconds=60)
        lighteningSpearDelay = Cooldown(milliseconds=960)
        lighteningSpearInterval = Cooldown(milliseconds=240)
        lighteningSpearDuration = Cooldown(milliseconds=3600)
        KeydownSkill.__init__(
            self=self,
            icon=lighteningSpearIcon,
            advanced=SkillAdvance.Hyper,
            level=level,
            max=max,
            keydowntime=lighteningSpearDuration
        )
        ThunderColdDamageAttribute.__init__(
            self=self,
            damage_point=lighteningSpearDamage,
            line=lighteningSpearAttackLine,
            castingCount=lighteningSpearAttackCount
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=lighteningSpearCooldown,
            isresetable=False
        )
        DurationAttribute.__init__(
            self=self,
            duration=lighteningSpearDuration,
            serverlack=False,
            isbuffmult=False
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=lighteningSpearDelay,
            applyAttackSpeed= False,
            special=False
        )
        IntervalAttribute.__init__(
            self=self,
            interval=lighteningSpearInterval
        )
        FinalAttackAttribute.__init__(
            self=self,
            finalAttack=블리자드_파이널어택
        )

    def SetChainLighteningDamage(self):
        return 150
    
    def UseSkill(self):
        if not isinstance(self.Owner, ABCCharacter):
            raise TypeError("스킬의 소유자가 설정되지 않앗음")
        
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        
        buff = self.ThunderAttackBuff()
        self.DecrementCold()

        if 라이트닝_스피어_강화_5th in self.Owner._PassiveSkillList:
            buff += 라이트닝_스피어_강화_5th().lighteningCoreReinforce

        lighteningSpearLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = buff)
        
        # 데미지가 유효하면 파이널어택을 발동시킴
        blizzardFinalLog = None
        if lighteningSpearLog is not None:
            
            blizzardFinalLog = self.UseFinalAttack()

        self.Done = True
        return [lighteningSpearLog, blizzardFinalLog]

    def Finish(self):
        buff = self.ThunderAttackBuff()
        self.DecrementCold()

        if 라이트닝_스피어_강화_5th in self.Owner._PassiveSkillList:
            buff += 라이트닝_스피어_강화_5th().lighteningCoreReinforce

        self.DamagePoint = 780
        FinishAttackLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = buff)

        # 데미지가 유효하면 파이널어택을 발동시킴
        blizzardFinalLog = None
        if FinishAttackLog is not None:
            
            blizzardFinalLog = self.UseFinalAttack()

        self.Done = True
        return [FinishAttackLog, blizzardFinalLog]
    
class 라이트닝_스피어_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        self.lighteningCoreReinforce = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level * 라이트닝_스피어().Advanced.value)
        self.lighteningCoreReinforce[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20

class 아이스_오라_사용(OnPressSkill, ThunderColdDamageAttribute, SummonAttribute, CooldownAttribute):
    def __init__(self, level=1):
        max = 1
        IceauraIcon = None
        OnPressSkill.__init__(
            self=self,
            icon= IceauraIcon,
            advanced=SkillAdvance.Hyper,
            level=level,
            max=max
        )
        ThunderColdDamageAttribute.__init__(
            self=self,
            damage_point=0,
            line=0,
            castingCount=0
        )
        SummonAttribute.__init__(
            self=self,
            duration=Cooldown(seconds=30),
            interval=Cooldown(milliseconds=300),
            mult = False
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=Cooldown(seconds=60),
            isresetable=False
        )

    def UseSkill(self):
        for key, value in list(self.Owner.SummonManager.Summons.items()):
            if isinstance(key.Skill, 아이스_오라):
                del self.Owner.SummonManager.Summons[key]
        self.IncrementCold()

    def EndSummon(self):
        buff = 아이스_오라()
        buff.Owner = self.Owner
        buff.Target = self.Target

        self.Owner.SummonManager.Add(buff)


class 아이스_오라(AutomateActivativeSkill, ThunderColdDamageAttribute, SummonAttribute):
    def __init__(self, level=1):
        max = 1
        IceauraIcon = None
        AutomateActivativeSkill.__init__(
            self=self,
            advanced=SkillAdvance.Hyper,
            level=level,
            max=max
        )
        ThunderColdDamageAttribute.__init__(
            self=self,
            damage_point=0,
            line=0,
            castingCount=0,
            
        )
        SummonAttribute.__init__(
            self=self,
            duration=Cooldown(seconds=9999),
            interval=Cooldown(milliseconds=960),
            mult = False
        )
    
    @classmethod
    def active(self):
        return False

    def UseSkill(self):
        self.IncrementCold()


# 5차 스킬
class 썬더_브레이크(OnPressSkill, ThunderColdDamageAttribute, SummonAttribute, SkillDelayAttribute, SkipableAttribute, StackAttribute, FinalAttackAttribute):
    

    def __init__(self, level=30):
        max = 30
        ThunderbreakIcon = None
        ThunderbreakDamagePoint = 925+38*level
        ThunderbreakAttackLine = 12
        ThunderbreakAttackCount = 8
        ThunderbreakInterval = Cooldown(milliseconds=360)
        ThunderbreakDuration = Cooldown(milliseconds = 2520)
        ThunderbreakAttackDelay = Cooldown(milliseconds=660)
        ThunderbreakSkipableList = [체인_라이트닝, 프로즌_오브,블리자드,라이트닝_스피어]
        
        OnPressSkill.__init__(
            self=self,
            icon=ThunderbreakIcon,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )
        ThunderColdDamageAttribute.__init__(
            self=self,
            damage_point=ThunderbreakDamagePoint,
            line=ThunderbreakAttackLine,
            castingCount=ThunderbreakAttackCount
        )
        SummonAttribute.__init__(
            self=self,
            duration=ThunderbreakDuration,
            interval=ThunderbreakInterval,
            mult=False
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=ThunderbreakAttackDelay,
            applyAttackSpeed=True,
            special=False
        )
        SkipableAttribute.__init__(
            self=self,
            combo_skill_list=ThunderbreakSkipableList,
            skip=[e().AttackDelay for e in ThunderbreakSkipableList]
        )
        StackAttribute.__init__(
            self=self,
            max_stack=ThunderbreakAttackCount,
            charged_stack=0,
            charge_cooltime=0
        )
        FinalAttackAttribute.__init__(
            self=self,
            finalAttack=블리자드_파이널어택
        )

    def UseSkill(self):
        # 몹 크기에 따른 썬브 히트수
        if self.Target.Size == DummySize.small:
            self.MaxStack = 2
        elif self.Target.Size == DummySize.medium:
            self.MaxStack = 3
        elif self.Target.Size == DummySize.large:
            self.MaxStack = 4
        
        
        if self.ChargedStack == self.Target.Size:
            return []
        
        # 썬브의 현재 누적 타수 설정    
        self.ChargedStack += 1
        self.DamagePoint *= 0.8

        if not isinstance(self.Owner, ABCCharacter):
            raise TypeError("스킬의 소유자가 설정되지 않앗음")
        
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        
        
        buff = self.ThunderAttackBuff()
        self.DecrementCold()

        # 데미지를 계산
        ThunderbreakLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = buff)

        blizzardFinalLog = None
        if ThunderbreakLog is not None:
            
            blizzardFinalLog = self.UseFinalAttack()

        self.Done = True
        return [ThunderbreakLog, blizzardFinalLog]

class 스피릿_오브_스노우(OnPressSkill, ThunderColdDamageAttribute, SummonAttribute, SkillDelayAttribute, CooldownAttribute):

    def __init__(self, level=30):
        max = 30
        SOSIcon = None

        SOSDamage = 850+34*level
        SOSAttackLine = 9
        SOSDuration = Cooldown(seconds=30)
        SOSInterval = Cooldown(seconds=3)
        SOSSummonDelay  = Cooldown(milliseconds=720)
        SOSCooldown = Cooldown(seconds=120)

        OnPressSkill.__init__(
            self=self,
            icon = SOSIcon,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )
        ThunderColdDamageAttribute.__init__(
            self=self,
            damage_point=SOSDamage,
            line=SOSAttackLine
        )
        SummonAttribute.__init__(
            self=self,
            duration=SOSDuration,
            interval=SOSInterval,
            mult=False
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=SOSSummonDelay,
            applyAttackSpeed=True
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=SOSCooldown,
            isresetable=False
        )

    def UseSkill(self):
        if not isinstance(self.Owner, ABCCharacter):
            raise TypeError("스킬의 소유자가 설정되지 않앗음")
        
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        
        buff = self.ColdAttackBuff()
        for _ in range(0,3):
            self.IncrementCold()

        SOSLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = buff)

        self.Done = True
        return [SOSLog]

class 아이스_에이지(OnPressSkill, ThunderColdDamageAttribute, SkillDelayAttribute, FinalAttackAttribute, CooldownAttribute):
    def __init__(self, level=30):
        max = 30
        IceAgeIcon = None
        IceAgeDamagePoint = 500+20*level
        IceAgeDamageLine = 10
        IceAgeCastingDelay = Cooldown(milliseconds=870)
        IceAgeCooldown = Cooldown(seconds=60)

        OnPressSkill.__init__(
            self=self,
            icon=IceAgeIcon,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )
        ThunderColdDamageAttribute.__init__(
            self=self,
            damage_point=IceAgeDamagePoint,
            line=IceAgeDamageLine
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=IceAgeCastingDelay,
            applyAttackSpeed=True
        )
        FinalAttackAttribute.__init__(self, finalAttack=블리자드_파이널어택)
        CooldownAttribute.__init__(
            self=self,
            cooldown=IceAgeCooldown,
            isresetable=False
        )


    def UseSkill(self):
        if not isinstance(self.Owner, ABCCharacter):
            raise TypeError("스킬의 소유자가 설정되지 않앗음")
        
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
      
        buff = self.ColdAttackBuff()
        self.IncrementCold

        IceAgeLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = buff)

        # 데미지가 유효하면 파이널어택을 발동시킴
        blizzardFinalLog = None
        if IceAgeLog is not None:
            
            blizzardFinalLog = self.UseFinalAttack()

        
        summon = 아이스_에이지_파편(level=self.Level)
        summon.Owner = self.Owner
        summon.Target = self.Target

        self.Owner.SummonManager.Add(summon)


        return [IceAgeLog, blizzardFinalLog]

class 아이스_에이지_파편(OnPressSkill, ThunderColdDamageAttribute, SummonAttribute):
    def __init__(self, level=30):
        max = 아이스_에이지().MaxLevel
        IceAgeIcon = None
        IceAgeSummonDamagePoint = 500+20*level
        IceAgeSummonDamageLine = 10
        
        IceAgeSummonDuraton = Cooldown(seconds=15)
        IceAgeSummonInterval = Cooldown(milliseconds=810)

        OnPressSkill.__init__(
            self=self,
            icon=IceAgeIcon,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )
        ThunderColdDamageAttribute.__init__(
            self=self,
            damage_point=IceAgeSummonDamagePoint,
            line=IceAgeSummonDamageLine
        )
        SummonAttribute.__init__(
            self=self,
            duration=IceAgeSummonDuraton,
            interval=IceAgeSummonInterval,
            mult=False
        )



    def UseSkill(self):
        if not isinstance(self.Owner, ABCCharacter):
            raise TypeError("스킬의 소유자가 설정되지 않앗음")
        
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
      
        buff = self.ColdAttackBuff()
        self.IncrementCold

        IceAgeLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = buff)

        

        return [IceAgeLog]

class 주피터_썬더(OnPressSkill, ThunderColdDamageAttribute, SummonAttribute, CooldownAttribute, SkillDelayAttribute, FinalAttackAttribute, StackAttribute):
    def __init__(self, level=30):
        max=30
        JupyterThunderIcon = None

        JupyterThunderDamage = 300+12*level
        JupyterThunderAttackLine = 8
        JupyterThunderCount = 30
        JupyterThunderDuration = Cooldown(milliseconds=9900)
        JupyterThunderInterval = Cooldown(milliseconds=330)
        JupyterThunderCooldown = Cooldown(seconds=120)
        JupyterThunderAttackDelay = Cooldown(milliseconds=810)


        OnPressSkill.__init__(
            self=self,
            icon=JupyterThunderIcon,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )        
        ThunderColdDamageAttribute.__init__(
            self=self,
            damage_point=JupyterThunderDamage,
            line=JupyterThunderAttackLine
        )
        SummonAttribute.__init__(
            self=self,
            duration=JupyterThunderDuration,
            interval=JupyterThunderInterval,
            mult=False
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=JupyterThunderCooldown,
            isresetable=False
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=JupyterThunderAttackDelay,
            applyAttackSpeed=True
        )
        FinalAttackAttribute.__init__(
            self=self,
            finalAttack=블리자드_파이널어택
        )
        StackAttribute.__init__(
            self=self,
            max_stack=JupyterThunderCount,
            charged_stack= 0,
            charge_cooltime=0
        )


    def UseSkill(self):
        if not isinstance(self.Owner, ABCCharacter):
            raise TypeError("스킬의 소유자가 설정되지 않앗음")
        
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        
        buff = self.ThunderAttackBuff()
        if self.ChargedStack% 5 == 0:
            self.DecrementCold()
        self.ChargedStack += 1

        JupyterThunderLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = buff)

        blizzardFinalLog = None
        if JupyterThunderLog is not None:
            
            blizzardFinalLog = self.UseFinalAttack()

        self.Done = True
        return [JupyterThunderLog, blizzardFinalLog]

class 스파이더_인_미러_썬콜(스파이더_인_미러, ThunderColdDamageAttribute):
    def __init__(self, level=30):
        스파이더_인_미러.__init__(self,level)

    # 썬콜의 스파이더 인 미러는 프로스트 이펙트의 효과를 받음
    def UseSkill(self):

        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        stat = self.ColdAttackBuff()

        spiderInMirrorLog = self.Target.TakeAttack(
            char = self.Owner,
            skill=self,
            add=stat
        )

        # 스인미 거울속의 거미 소환
        summon = 스파이더_인_미러_거울속의_거미_썬콜(level=self.Level)
        summon.Owner = self.Owner
        summon.Target = self.Target

        self.Owner.SummonManager.Add(summon)


        return [spiderInMirrorLog]
    

class 스파이더_인_미러_거울속의_거미_썬콜(스파이더_인_미러_거울속의_거미, ThunderColdDamageAttribute):
 
    def __init__(self, level: int):
        스파이더_인_미러_거울속의_거미.__init__(
            self=self,
            level=스파이더_인_미러_썬콜().Level
        )
    

    def UseSkill(self):
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        stat = self.ColdAttackBuff()


        spiderInMirrorLog = self.Target.TakeAttack(
            char = self.Owner,
            skill=self,
            add=stat
        )
        return [spiderInMirrorLog]
    
class 크레스트_오브_더_솔라_썬콜(크레스트_오브_더_솔라, ThunderColdDamageAttribute):
    def __init__(self):
        크레스트_오브_더_솔라.__init__(self=self)

    def UseSkill(self):
        stat = self.ColdAttackBuff()
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        

        SunRiseLog = self.Target.TakeAttack(
            char = self.Owner,
            skill=self,
            add=stat
        )

        # 스인미 거울속의 거미 소환
        summon = 크레스트_오브_더_솔라_불꽃의_문양_썬콜()
        summon.Owner = self.Owner
        summon.Target = self.Target

        self.Owner.SummonManager.Add(summon)


        return [SunRiseLog]
    

class 크레스트_오브_더_솔라_불꽃의_문양_썬콜(크레스트_오브_더_솔라_불꽃의_문양, ThunderColdDamageAttribute):
    def __init__(self):
        크레스트_오브_더_솔라_불꽃의_문양.__init__(
            self=self
        )

    def UseSkill(self):
        
        stat = self.ColdAttackBuff()

        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        

        SunRiseLog = self.Target.TakeAttack(
            char = self.Owner,
            skill=self,
            add=stat
        )
        return [SunRiseLog]

class 프로즌_라이트닝(OriginSkill, ThunderColdDamageAttribute, SkillDelayAttribute, CooldownAttribute):
    def __init__(self, level=30):
        FrozenLighteningIcon = None
        FrozenLightening1stDamage = 1920
        FrozenLightening1stDamageLine = 5
        self.FrozenLightening1stCount = 10

        self.FrozenLightening2stDamage = 4200
        self.FrozenLightening2stDamageLine = 8
        self.FrozenLightening2stCount = 4
        self.FrozenLighteningFinishCount = 22


        FrozenLightening1stCastingdelay = Cooldown(milliseconds=4020)
        FrozenLighteningTimingTable = [Cooldown(seconds=1)] + [Cooldown(milliseconds=270) for _ in range(0, self.FrozenLightening1stCount)] \
        + [Cooldown(milliseconds=90) for _ in range(0, self.FrozenLightening2stCount)]
        
        FrozenlighteningCooldown = Cooldown(seconds=360)

        OriginSkill.__init__(
            self=self,
            icon=FrozenLighteningIcon,
            advanced=SkillAdvance.Sixth,
            level=level,
            max=max,
            timingTable=FrozenLighteningTimingTable
        )
        ThunderColdDamageAttribute.__init__(
            self=self,
            damage_point=FrozenLightening1stDamage,
            line=FrozenLightening1stDamageLine,
            castingCount=self.FrozenLightening1stCount
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=FrozenLightening1stCastingdelay,
            applyAttackSpeed=False
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=FrozenlighteningCooldown,
            isresetable=False
        )

    def UseSkill(self):
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        
        
        buff = self.ThunderAttackBuff()
        
        if self.index > self.CastingCount:
            self.DamagePoint = self.FrozenLightening2stDamage
            self.AttackLine = self.FrozenLightening2stDamageLine
            # 공격기 소환
            summon = 프로즌_라이트닝_추가타격()
            summon.Owner = self.Owner
            summon.Target = self.Target
            self.Owner.BuffManager.Add(summon)


        FrozenLighteningLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = buff)

        return [FrozenLighteningLog]

    def Finish(self):
        # 알덩이 소환
        for _ in range(0, self.FrozenLighteningFinishCount):
            summon = 프로즌_라이트닝_얼음파편()
            summon.Owner = self.Owner
            summon.Target = self.Target
            self.Owner.ProjectileManager.Add(summon)
    
class 프로즌_라이트닝_얼음파편(OnPressSkill, ProjectileAttribute, ThunderColdDamageAttribute, FinalAttackAttribute):
    def __init__(self):


        sup = 프로즌_라이트닝()
        max = sup.MaxLevel
        subFrozenIcon = sup.Icon
        subFrozenDamage = 1200
        subFrozenAttackLine = 3

        OnPressSkill.__init__(
            self=self,
            icon=subFrozenIcon,
            advanced=SkillAdvance.Sixth,
            level=sup.Level,
            max=max
        )
        ProjectileAttribute.__init__(
            self=self,
            maximumTime=1
        )
        ThunderColdDamageAttribute.__init__(
            self=self,
            damage_point=subFrozenDamage,
            line=subFrozenAttackLine
        )
        FinalAttackAttribute.__init__(
            self=self,
            finalAttack=블리자드_파이널어택
        )

    def UseSkill(self):
        if not isinstance(self.Owner, ABCCharacter):
            raise TypeError("스킬의 소유자가 설정되지 않앗음")
        
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        
        # 번개 속성 공격 시 빙결스택에 따른 버프 효과를 받아옴
        
        buff = self.ColdAttackBuff()
        self.IncrementCold()
        
        subFrozenLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = buff)


        # 데미지가 유효하면 파이널어택을 발동시킴
        blizzardFinalLog = None
        if subFrozenLog is not None:
            
            blizzardFinalLog = self.UseFinalAttack()

        return [subFrozenLog, blizzardFinalLog]


class 프로즌_라이트닝_추가타격(OnPressSkill, ThunderColdDamageAttribute, CooldownAttribute, DurationAttribute, BuffAttribute):
    
    def __init__(self, level = 30):
        max = 30
        FrozenAddDamage = 1800
        FrozenAddAttackLine = 5
        FrozenAddCooldown = Cooldown(seconds=2)
        FrozenAddDuration = Cooldown(seconds=30)
        self.AttCount = 0
        AutomateActivativeSkill.__init__(
            self=self,
            advanced=SkillAdvance.Sixth,
            level=level,
            max=max
        )
        ThunderColdDamageAttribute.__init__(
            self=self,
            damage_point=FrozenAddDamage,
            line=FrozenAddAttackLine
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=FrozenAddCooldown,
            isresetable=False
        )
        DurationAttribute.__init__(
            self=self,
            duration=FrozenAddDuration,
            serverlack=True,
            isbuffmult=False
        )
        BuffAttribute.__init__(
            self=self,
            stat=SpecVector()
        )

    @property
    def BuffStat(self):
        if self.AttCount >= 15:
            return SpecVector()

        if self.Owner.ReadyFor(type(self)):
            self.Owner.CooldownManager.Count(type(self))
            self.Owner.ProjectileManager.Add(self, isImmediate=True)
            self.AttCount += 1
        
        return SpecVector()
    
    def UseSkill(self):
        if not isinstance(self.Owner, ABCCharacter):
            raise TypeError("스킬의 소유자가 설정되지 않앗음")
        
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        
        # 번개 속성 공격 시 빙결스택에 따른 버프 효과를 받아옴
        
        buff = self.ThunderAttackBuff()
        self.DecrementCold()
        
        subFrozenLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = buff)


        
        return [subFrozenLog]

