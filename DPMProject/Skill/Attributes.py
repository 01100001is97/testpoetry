from Core import Cooldown
from Core.SpecElements import SpecVector
from Core.Job import JobName, JobGroup, JobType
from Core.Condition import ConditionEnum
from abc import ABC, abstractmethod
from Core.Cooldown import Cooldown
from Core.ABCSkill import Skill
from copy import deepcopy
import math

class DurationAttribute:
    """
    스킬의 지속 시간 속성을 나타내는 클래스입니다.

    Args:
        duration (Cooldown): 스킬의 지속 시간
        serverlack (bool): 서버 라그 여부
        isbuffmult (bool): 버프 스킬의 경우 여러 스킬의 효과가 중첩되는지 여부

    Raises:
        ValueError: duration이 Cooldown의 인스턴스가 아닌 경우 발생합니다.
        ValueError: serverlack 또는 isbuffmult가 bool의 인스턴스가 아닌 경우 발생합니다.
    """
    SERVER_LACK = Cooldown(seconds=3)

    def __init__(self, duration: Cooldown, serverlack: bool, isbuffmult: bool):
        self._Duration = duration
        self._ServerLack = serverlack
        self._IsBuffMult = isbuffmult
        

    @property
    def Duration(self):
        return self._Duration
        
        
                
    @Duration.setter
    def Duration(self, duration: Cooldown):
        if not isinstance(duration, Cooldown):
            raise ValueError("duration must be an instance of Cooldown")
        
        
        
        self._Duration = duration

    @property
    def ServerLack(self):
        return self._ServerLack

    @ServerLack.setter
    def ServerLack(self, serverlack: bool):
        if not isinstance(serverlack, bool):
            raise ValueError("serverlack must be an instance of bool")
        self._ServerLack = serverlack

    @property
    def IsBuffMult(self):
        return self._IsBuffMult

    @IsBuffMult.setter
    def IsBuffMult(self, isbuffmult: bool):
        if not isinstance(isbuffmult, bool):
            raise ValueError("isbuffmult must be an instance of bool")
        self._IsBuffMult = isbuffmult

class BuffAttribute:
    """
    스킬의 버프 속성을 나타내는 클래스입니다.

    Args:
        stat (SpecVector): 스킬의 버프로 인해 증가되는 스탯

    Raises:
        ValueError: stat이 SpecVector의 인스턴스가 아닌 경우 발생합니다.
    """
    def __init__(self, stat: SpecVector):
        self._BuffStat = stat

    @property
    def BuffStat(self):
        return self._BuffStat

    @BuffStat.setter
    def BuffStat(self, stat: SpecVector):
        if not isinstance(stat, (SpecVector, callable)):
            raise ValueError("stat must be an instance of SpecVector")
        self._BuffStat = stat

class DebuffAttribute:
    """
    스킬의 디버프 속성을 나타내는 클래스입니다.

    Args:
        debuff_stat (SpecVector): 스킬의 디버프로 인해 감소되는 스탯
        condition (list[ConditionEnum]): 디버프 상태

    Raises:
        ValueError: debuff_stat이 SpecVector의 인스턴스가 아닌 경우 발생합니다.
        ValueError: condition이 ConditionEnum의 인스턴스 리스트가 아닌 경우 발생합니다.
    """
    def __init__(self, debuff_stat: SpecVector, condition: list[ConditionEnum]):
        self.DebuffStat = debuff_stat
        self.Condition = condition

    @property
    def DebuffStat(self):
        return self._DebuffStat

    @DebuffStat.setter
    def DebuffStat(self, debuff_stat: SpecVector):
        if not isinstance(debuff_stat, SpecVector):
            raise ValueError("debuff_stat must be an instance of SpecVector")
        self._DebuffStat = debuff_stat

    @property
    def Condition(self):
        return self._Condition

    @Condition.setter
    def Condition(self, condition: list[ConditionEnum]):
        if not all(isinstance(c, ConditionEnum) for c in condition):
            raise ValueError("condition must be a list of instances of ConditionEnum")
        self._Condition = condition
         
class MasteryAttribute:
    """
    스킬의 마스터리 속성을 나타내는 클래스입니다.

    Args:
        mastery (int): 버프 마스터리 수치

    Raises:
        ValueError: mastery가 정수가 아닌 경우 발생합니다.
    """
    def __init__(self, mastery: int):
        self.Mastery = mastery

    @property
    def Mastery(self):
        return self._Mastery

    @Mastery.setter
    def Mastery(self, mastery: int):
        if not isinstance(mastery, int):
            raise ValueError("mastery must be an integer")
        self._Mastery = mastery

class DamageAttribute:
    """
    스킬의 데미지 속성을 나타내는 클래스입니다.

    Args:
        damage_point (int): 스킬의 데미지 포인트

    Raises:
        ValueError: damage_point가 정수가 아닌 경우 발생합니다.
    """
    MAX_ATTACK_LINE = 15
    def __init__(self, damage_point: int, line: int,castingCount: int = 1, ):
        
        self._DamagePoint = damage_point
        self._CastingCount = castingCount
        self._AttackLine = line

    @property
    def DamagePoint(self):
        return self._DamagePoint

    @DamagePoint.setter
    def DamagePoint(self, damage_point: int):
        if not isinstance(damage_point, (int,float)):
            raise ValueError("damage_point must be an integer")
        self._DamagePoint = damage_point

    @property
    def CastingCount(self):
        return self._CastingCount
    
    @CastingCount.setter
    def CastingCount(self, count:int):
        if not isinstance(count, int):
            raise ValueError("Count must be an integer")
        
        self._CastingCount = count

    @property
    def AttackLine(self):
        return self._AttackLine
    
    @AttackLine.setter
    def AttackLine(self, line:int):
        if not isinstance(line, int):
            raise ValueError("line must be an integer")
        
        if line > self.MAX_ATTACK_LINE:
            raise ValueError("line must smaller than self.ATTAK_LINE")
        
        self._AttackLine = line
        
class NonlinearIntervalAttribute:
    """
    비선형 쿨타임 간격을 가진 스킬 효과의 적용 간격.

    Args:
        intervals (list): 비선형 쿨타임 간격을 표현하는 리스트
        condition (function): 다음 인터벌로 넘어갈지 결정하는 람다 함수
    """
    def __init__(self, intervals: list, condition: callable):
        if not isinstance(intervals, list):
            raise ValueError("intervals must be a list")
        if not isinstance(condition, type(lambda:0)):
            raise ValueError("condition must be a lambda function")

        self._intervals = [intervals[0]] + intervals
        self._condition = condition
        self._index = 0

    @property
    def Interval(self):
        # 리스트의 마지막 인덱스에 도달하면 매우 긴 쿨타임을 반환
        if self._index >= len(self._intervals):
            return Cooldown(minutes=99999)
        else:
            interval = self._intervals[self._index]
            if self._condition():  # condition 함수가 참을 반환하면 index 증가
                self._index += 1
            return interval

class IntervalAttribute:
    """
    스킬 효과의 적용 간격

    Args:
        interval (Cooldown): 스킬 효과 적용 간격

    Raises:
        ValueError: interval이 Cooldown의 인스턴스가 아닌 경우 발생합니다.
    """
    def __init__(self, interval: Cooldown):
        self._Interval = interval

    @property
    def Interval(self):
        return self._Interval

    @Interval.setter
    def Interval(self, interval: Cooldown):
        if not isinstance(interval, Cooldown):
            raise ValueError("interval must be an instance of Cooldown")
        self._Interval = interval

class CooldownAttribute:
    """
    스킬의 쿨다운 속성을 나타내는 클래스입니다.

    Args:
        cooldown (Cooldown): 스킬의 쿨다운

    Raises:
        ValueError: cooldown이 Cooldown의 인스턴스가 아닌 경우 발생합니다.
    """
    def __init__(self, cooldown: Cooldown, isresetable:bool):
        self._Cooldown = cooldown
        self._IsResetable = isresetable

    @property
    def SkillCooldown(self):
        return self._Cooldown

    @SkillCooldown.setter
    def SkillCooldown(self, cooldown: Cooldown):
        if not isinstance(cooldown, Cooldown):
            raise ValueError("cooldown must be an instance of Cooldown")
        self._Cooldown = cooldown

    @property
    def IsResetable(self):
        return self._IsResetable
    
    @IsResetable.setter
    def IsResetable(self, condition:bool):
        if not isinstance(condition, bool):
            raise ValueError("condition must be a bool type")
        self._IsResetable = condition

class ChargedCooldownAttribute(CooldownAttribute):
    def __init__(self, cooldown: Cooldown, isresetable: bool, maxcharge: int, isCooldownable: bool):
        self._MaxBuffCharge = maxcharge
        self._IsCooldownable = isCooldownable
        CooldownAttribute.__init__(self, cooldown, isresetable)

    @property
    def MaxBuffCharge(self):
        return self._MaxBuffCharge
    
    @property
    def IsCooldownable(self):
        return self._IsCooldownable

class SkillDelayAttribute:
    """
    스킬의 공격 딜레이 속성을 나타내는 클래스입니다. 

    Args:
        delay (Cooldown): 스킬의 공격 딜레이

    Raises:
        ValueError: delay가 Cooldown의 인스턴스가 아닌 경우 발생합니다.
    """
    def __init__(self, casting_delay: Cooldown, applyAttackSpeed: bool, special = False):
        delay = None
        if applyAttackSpeed == True:
            delay = Cooldown(milliseconds=round(casting_delay.total_milliseconds() * (3/4) / 30)*30)
        else:
            delay = casting_delay
        
        if special == True:
            delay = casting_delay
        self._AttackDelay = delay

    @property
    def AttackDelay(self):
        return self._AttackDelay

    @AttackDelay.setter
    def AttackDelay(self, delay: Cooldown):
        if not isinstance(delay, Cooldown):
            raise ValueError("delay must be an instance of Cooldown")
        self._AttackDelay = delay

class SkipableAttribute:
    """
    스킬의 콤보 속성을 나타내는 클래스입니다.

    Args:
        combo_skill_list (list): 콤보로 실행되는 스킬 목록
        skip (Cooldown): 스킬 콤보 시 건너뛰는 쿨다운
        casting_delay (Cooldown): 스킬의 시전 딜레이

    Raises:
        ValueError: combo_skill_list가 리스트가 아닌 경우 발생합니다.
        ValueError: skip이 Cooldown의 인스턴스가 아닌 경우 발생합니다.
    """

    def __init__(self, combo_skill_list: list, skip: list[Cooldown]):
        
        self._ComboSkillList = combo_skill_list
        self.Skip = skip

    @property
    def ComboSkillList(self):
        return self._ComboSkillList

    @ComboSkillList.setter
    def ComboSkillList(self, combo_skill_list: list):
        if not isinstance(combo_skill_list, list):
            raise ValueError("combo_skill_list must be a list")
        self._ComboSkillList = combo_skill_list

    @property
    def Skip(self):
        return self._Skip

    @Skip.setter
    def Skip(self, skip: list[Cooldown]):
        if not all(isinstance(i, Cooldown) for i in skip):
            raise ValueError("All elements in skip must be an instance of Cooldown")
        self._Skip = skip


class JobNameAttribute:
    """
    스킬의 직업 이름 속성을 나타내는 클래스입니다.

    Args:
        job (JobName): 스킬을 사용하는 직업 이름

    Raises:
        ValueError: job이 JobName의 인스턴스가 아닌 경우 발생합니다.
    """
    def __init__(self, job: JobName):
        if not isinstance(job, JobName):
            raise ValueError("job must be an instance of JobName")
        self._Job = job

class JobGroupAttribute:
    """
    스킬의 직업군 속성을 나타내는 클래스입니다.

    Args:
        job_group (JobGroup): 스킬을 사용하는 직업군

    Raises:
        ValueError: job_group이 JobGroup의 인스턴스가 아닌 경우 발생합니다.
    """
    def __init__(self, job_group: JobGroup):
        self.JobGroup = job_group

    @property
    def JobGroup(self):
        return self._JobGroup

    @JobGroup.setter
    def JobGroup(self, job_group: JobGroup):
        if not isinstance(job_group, JobGroup):
            raise ValueError("job_group must be an instance of JobGroup")
        self._JobGroup = job_group

class JobTypeAttribute:
    """
    스킬의 직업 유형 속성을 나타내는 클래스입니다.

    Args:
        job_type (JobType): 스킬을 사용하는 직업 유형

    Raises:
        ValueError: job_type이 JobType의 인스턴스가 아닌 경우 발생합니다.
    """
    def __init__(self, job_type: JobType):
        self.JobType = job_type

    @property
    def JobType(self):
        return self._JobType

    @JobType.setter
    def JobType(self, job_type: JobType):
        if not isinstance(job_type, JobType):
            raise ValueError("job_type must be an instance of JobType")
        self._JobType = job_type

class StackAttribute:
    """
    스킬의 스택 속성을 나타내는 클래스입니다.

    Args:
        max_stack (int): 최대 스택 수
        charged_stack (int): 충전된 스택 수
        charge_cooltime (int): 스택 충전 쿨타임

    Raises:
        ValueError: max_stack이 정수가 아닌 경우 발생합니다.
        ValueError: charged_stack이 정수가 아닌 경우 발생합니다.
        ValueError: charge_cooltime이 정수가 아닌 경우 발생합니다.
    """
    def __init__(self, max_stack: int, charged_stack: int, charge_cooltime: int):
        self.MaxStack = max_stack
        self.nowStack = charged_stack
        self.ChargeCooltime = charge_cooltime

    @property
    def MaxStack(self):
        return self._MaxStack

    @MaxStack.setter
    def MaxStack(self, max_stack: int):
        if not isinstance(max_stack, int):
            raise ValueError("max_stack must be an integer")
        self._MaxStack = max_stack

    @property
    def nowStack(self):
        return self._ChargedStack

    @nowStack.setter
    def nowStack(self, charged_stack: int):
        if not isinstance(charged_stack, int):
            raise ValueError("charged_stack must be an integer")
        self._ChargedStack = charged_stack

    @property
    def ChargeCooltime(self):
        return self._ChargeCooltime

    @ChargeCooltime.setter
    def ChargeCooltime(self, charge_cooltime: int):
        if not isinstance(charge_cooltime, int):
            raise ValueError("charge_cooltime must be an integer")
        self._ChargeCooltime = charge_cooltime

class DOTAttribute:
    def __init__(self, dotdamage: int, duration:Cooldown, interval:Cooldown):
        self.DOTDuration = duration
        self.DOTDamagePoint = dotdamage
        self.DOTInterval = interval

class CombatOrdersAttribute:

    def __init__(self):
        self.IsCombat = None
        self.IsApplied = False

   
    # 쓸만한 컴뱃오더스: false, 찐 컴뱃 true
    @property
    def IsCombat(self):
        return self._IsCombat
    
    @IsCombat.setter
    def IsCombat(self, combat:bool):
        if not isinstance(combat, bool) and combat is not None:
            raise ValueError("combat must be an instance of bool")
        self._IsCombat = combat

    @property
    def IsApplied(self):
        return self._IsApplied
    
    @IsApplied.setter
    def IsApplied(self, applied:bool):
        if not isinstance(applied, bool):
            raise ValueError("applied must be an instance of bool")
        self._IsApplied = applied

    def ApplyCombat(self, isOriginal: bool):
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


class MoveAttribute:
    pass

class FinalAttackAttribute:
    def __init__(self, finalAttack:Skill):
        self._FinalAttack = finalAttack
        

class SummonAttribute(DurationAttribute, IntervalAttribute):
    def __init__(self, duration: Cooldown, interval: Cooldown, mult: bool):
        DurationAttribute.__init__(
            self,
            duration=duration,
            serverlack=False,
            isbuffmult=mult
        )
        IntervalAttribute.__init__(self, interval=interval)
        
    @abstractmethod
    def EndSummon(self):
        pass

class BuffDurationAttribute:

    def __init__(self, duration: int):
        if not 0<duration<=55:
            raise AttributeError("벞지 스킬 최대값은 55")
        self.BuffDurationOption = duration

class ProjectileAttribute:
    def __init__(self, maximumTime:int) -> None:
        self.Maximum = maximumTime

class ChannelingAttribute:
    def __init__(self, time:Cooldown):
        self.ChannelingTime = time
