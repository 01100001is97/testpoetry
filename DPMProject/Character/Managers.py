from Core.Cooldown import Cooldown, TIME_UNIT, TIME_ZERO
from collections import defaultdict
from Core.ABCSkill import Skill, AutomateActivativeSkill, OriginSkill
from Core.SpecElements import SpecVector, CreateSpecVector, CoreStat
from Skill.Attributes import *
from copy import deepcopy
import random

class CooldownManager:
    """CooldownManager는 스킬의 쿨타임을 관리합니다.

    각 스킬에 대한 쿨다운은 defaultdict를 사용하여 저장되며, 쿨타임이 0이되면 해당 스킬이 사전에서 삭제됩니다.

    Attributes:
        Cooldowns: 각 스킬에 대한 쿨타임을 저장하는 딕셔너리입니다.
        Cap: 쿨타임 상한 값을 저장하는 속성입니다. 0~8의 정수값을 가질 수 있습니다.
        Mercedes: 메르세데스 옵션 값을 저장하는 속성입니다. 5 또는 6의 정수값을 가질 수 있습니다.
        Reset: 쿨타임 리셋 값을 저장하는 속성입니다. 0~100의 정수값을 가질 수 있습니다.
    """
    def __init__(self):
        self.Cooldowns = defaultdict(Cooldown)
        # 스택형 스킬은 쿨타임 적용이 까다로우므로, 별도의 리스트를 둬서 따로 관리함
        self.StackCooldowns = defaultdict(list)
        self._Cap = 0
        self._Mercedes = 0
        self._Reset = 0

    @property
    def Cap(self):
        """Cap 속성의 getter입니다."""
        return self._Cap

    @Cap.setter
    def Cap(self, value):
        """Cap 속성의 setter입니다."""
        if not isinstance(value, int):
            raise TypeError("Cap must be an integer.")
        if not (0 <= value <= 8):
            raise ValueError("Cap value must be between 0 and 8.")
        self._Cap = value

    
    @property
    def Mercedes(self):
        """Mercedes 속성의 getter입니다."""
        return self._Mercedes

    @Mercedes.setter
    def Mercedes(self, value):
        """Mercedes 속성의 setter입니다."""
        if not isinstance(value, int):
            raise TypeError("Mercedes must be an integer.")
        if value not in (5, 6):
            raise ValueError("Mercedes value must be either 5 or 6.")
        self._Mercedes = value*0.01


    @property
    def Reset(self):
        """Reset 속성의 getter입니다."""
        return self._Reset

    @Reset.setter
    def Reset(self, value):
        """Reset 속성의 setter입니다."""
        if not isinstance(value, int):
            raise TypeError("Reset must be an integer.")
        if not (0 <= value <= 100):
            raise ValueError("Reset value must be between 0 and 100.")
        self._Reset = value

    def isReady(self, skill:Skill) -> bool:
        if self.GetRemainingCooldown(skill) > TIME_ZERO:
            return False
        elif self.GetRemainingCooldown(skill) == TIME_ZERO:
            return True
        else:
            raise AttributeError("스킬의 쿨다운에 의도치 않은 값이 설정되어 있음")


    def Count(self, skill: Skill):
        """스킬의 쿨타임을 등록하거나 업데이트합니다."""
        # TODO: 쿨타임 초기화 로직 구현
        if not issubclass(skill, Skill):    
            raise TypeError("Skill must be a callable")
        
        if not issubclass(skill, CooldownAttribute):
            raise TypeError("CooldownAttribute를 상속해야 관리할 수 있음")
        
        if not self.isReady(skill):
            return False

        # 스택형 스킬은 쿨타임 적용이 까다로우므로, 별도의 리스트를 둬서 따로 관리함
        if issubclass(skill, ChargedCooldownAttribute):
            # 이미 스택이 존재하는 경우라서 사용 가능한 경우
            stackedCool = self.StackCooldowns[skill]
            if len(stackedCool) == 0:
                # 스택형 스킬인데 쿨타임 감소가 적용되는 경우(메여축 등 특수케이스)
                if skill().IsCooldownable:
                    self.StackCooldowns[skill] = [skill().MaxBuffCharge-1, skill().SkillCooldown*(1-self.Mercedes) - Cooldown(seconds=self.Cap)]
                # 스택형 스킬인데 쿨타임 감소 적용 안되는 경우(일반적 경우)
                else:
                    self.StackCooldowns[skill] = [skill().MaxBuffCharge-1, skill().SkillCooldown]
            # 스킬이 등록되어 있고 스택이 존재하는 경우 스택만 감소시킴
            else:
                if self.StackCooldowns[skill][0] > 0:
                    self.StackCooldowns[skill][0] = self.StackCooldowns[skill][0] -1
                else:
                    raise AttributeError("스택형 스킬에 스택이 없는데 사용을 시도함")
        # 일반 스킬들의 쿨타임 관리
        else:            
            # 자동 발동 스킬은 쿨감 안먹음(시프 커닝, 일격필살 등)
            if issubclass(skill, (AutomateActivativeSkill, OriginSkill)):
                self.Cooldowns[skill] = skill().SkillCooldown
            # 일반 스킬은 쿨타임 감소가 항상 먹고,
            else:
                self.Cooldowns[skill] = skill().SkillCooldown*(1-self.Mercedes) - Cooldown(seconds=self.Cap)
                

        return True

    def Tick(self):
        """모든 스킬의 쿨타임을 감소시킵니다."""
        # 일반 스킬의 쿨타임 감소
        for skill, cool in list(self.Cooldowns.items()):
            newCool = deepcopy(max(TIME_ZERO, cool - TIME_UNIT))
            if newCool == TIME_ZERO:                    
                del self.Cooldowns[skill]
            else:
                self.Cooldowns[skill] = Cooldown(cooldown=newCool)

        # 스택형 쿨타임 스킬의 쿨타임 감소
        for skill, stackCool in list(self.StackCooldowns.items()):
            newCool = deepcopy(max(TIME_ZERO, stackCool[1] - TIME_UNIT))
            # 스택의 쿨타임이 모두 찬 경우
            if newCool == TIME_ZERO:
                # 스택의 최대치까지만 상승해야함
                maxstack = skill().MaxBuffCharge
                if self.StackCooldowns[skill][0] == maxstack:
                    self.StackCooldowns[skill] = [stackCool[0]+1,TIME_ZERO]
                # 스택의 상승이 최대치가 되지 않는 경우
                else:
                    if skill().IsCooldownable:
                        self.StackCooldowns[skill] = [stackCool[0]+1, skill().SkillCooldown*(1-self.Mercedes) - Cooldown(seconds=self.Cap)]
                    else:
                        self.StackCooldowns[skill] = [stackCool[0]+1, skill().SkillCooldown]
            # 스택의 쿨타임이 모두 차지 않은 경우 쿨타임 갱신함
            else:
                self.StackCooldowns[skill] = [stackCool[0], Cooldown(cooldown=newCool)]
            
    

    def GetRemainingCooldown(self, skill:Skill):
        """특정 스킬의 남은 쿨타임을 반환합니다."""
        if not issubclass(skill, Skill):
            raise TypeError("Skill must be a callable")
        
        # 스택형 쿨타임 스킬의 경우 별도로 관리함
        if issubclass(skill, ChargedCooldownAttribute):
            stackedCool = self.StackCooldowns[skill]
            # 스킬이 쿨타임 매니저에 등록되어 있지 않은 경우
            if len(stackedCool) == 0:
                # 스킬이 사용 가능하다고 알림
                return TIME_ZERO
            # 스킬이 쿨타임 매니저에 등록되어 있고 스택이 남아있는 경우
            elif stackedCool[0] > 0:
                # 스킬이 사용 가능하다고 알림
                return TIME_ZERO
            else:
                # 스킬이 등록되어 있고 남은 스택이 없는 경우 쿨타임이 있음을 반환
                return self.StackCooldowns[skill][1]
        # 스택형 버프가 아닌 경우 쿨타임 반환
        else:
            return self.Cooldowns[skill]
    
    def __getitem__(self, skill):
        """특정 스킬의 남은 쿨타임을 반환합니다."""
        return self.GetRemainingCooldown(skill=skill)
    
    def __iter__(self):
        return iter(self.Cooldowns.items())
    

class OnAttackManager(CooldownManager):
    def __init__(self):
        super().__init__()

class BuffManager:
    """
    BuffManager 클래스는 스킬의 쿨다운, 버프 속성, 지속시간 등을 관리합니다.
    각각의 스킬은 특정 속성을 상속받아야 하며, 그렇지 않으면 TypeError를 발생시킵니다.

    Raises:
        TypeError: 스킬이 호출 가능한 객체가 아닌 경우
        TypeError: 스킬이 CooldownAttribute를 상속받지 않은 경우
        TypeError: 스킬이 BuffAttribute를 상속받지 않은 경우
        TypeError: 스킬이 DurationAttribute를 상속받지 않은 경우

    Returns:
        None
    """
    # TODO: 대입할때 deepcopy를 사용할 것
    def __init__(self):
        self.BuffList = list()
        

    def Add(self, skill: Skill):
        # 추가하려는 스킬과 같은 타입의 스킬이 이미 BuffList에 있는지 확인
        if any(isinstance(buff.Skill, type(skill)) for buff in self.BuffList):
            return  # 이미 같은 타입의 스킬이 있으므로 함수를 종료
        
        if not issubclass(type(skill), Skill):    
            raise TypeError("Skill must be a callable")
        
        
        if not issubclass(type(skill), (BuffAttribute,DebuffAttribute)):
            raise TypeError("버프 스킬만 관리함")
        
        if not issubclass(type(skill), DurationAttribute):
            raise TypeError("버프 지속시간이 필요함")
        


        self.BuffList.append(Buff(skill))

    def GetBuff(self):
        """
        현재 BuffList에 있는 모든 버프의 통계를 반환합니다.

        Returns:
            SpecVector: 현재 버프 통계
        """
        result = SpecVector()
        for buff in self.BuffList:
            if hasattr(buff.Skill, 'DebuffStat'):
                isCallable = buff.Skill.DebuffStat
            else:
                isCallable = buff.Skill.BuffStat
            if callable(isCallable):
                # 스킬의 남은 지속시간 혹은 여러 조건들을 대입. 람다함수를 불러와서 처리함
                result += isCallable(buff.GetRealDuration() - buff.SkillLeftDuration)
            else:
                result += isCallable
        return result
    
    def Tick(self):
        """
        BuffList의 모든 버프의 지속 시간을 감소시킵니다.
        만약 버프의 지속 시간이 0이 되면 해당 버프를 BuffList에서 제거합니다.

        Returns:
            None
        """
        for buff in reversed(self.BuffList):
            if buff.Tick() == False:
                self.BuffList.remove(buff)



class Buff:
    """
    Buff 클래스는 개별 버프의 지속 시간을 관리합니다.
    각 버프는 Skill 객체를 참조하며, 지속 시간은 Skill 객체의 Duration 속성에서 얻습니다.

    Args:
        skill (Skill): 버프와 관련된 스킬 객체

    Returns:
        None
    """
    def __init__(self, skill:Skill):
        self.Skill = skill  

        self.SkillLeftDuration = self.GetRealDuration()
 
    def GetRealDuration(self):
        add = Cooldown()
        if self.Skill.ServerLack == True:
            add = Cooldown(seconds = 3)
        mult = 1
        if self.Skill.IsBuffMult == True:
            mult = (self.Skill.Owner._BuffDuration/100 + 1) 
        return self.Skill.Duration * mult + add

    def Tick(self):
        """
        버프의 지속 시간을 감소시킵니다.
        만약 버프의 지속 시간이 0이 되면 False를 반환하며, 그렇지 않으면 None을 반환합니다.

        Returns:
            bool or None: 버프의 지속 시간이 0이 되면 False, 아니면 None
        """
        if self.SkillLeftDuration == TIME_ZERO:
            return False
        else:            
            self.SkillLeftDuration -= TIME_UNIT
            

class ProjectileManager:
    def __init__(self) -> None:
        self.Scheduler = defaultdict(lambda: Cooldown(seconds=random.random()))

    def Add(self, skill:Skill, isImmediate=False):
        if not isinstance(skill, Skill):
            raise TypeError("skill must be a Skill type")
        
        self.Scheduler[skill] 
        if isImmediate:
            self.Scheduler[skill] = Cooldown()

    def Tick(self):
        result = []
        for projectile, cool in list(self.Scheduler.items()):
            cool.update()
            if cool == TIME_ZERO:
                projLogs = projectile.UseSkill()
                    
                if None !=projLogs:
                    for log in projLogs:
                        if log is not None:
                            result.append(log)

                del self.Scheduler[projectile]
        return result
        

class SummonManager:
    """소환수 인스턴스를 입력받아서 관리함
    """
    def __init__(self):
        self.Summons = defaultdict(Cooldown)
        
        
    def Add(self, skill: Skill):
        # 소환수 인스턴스를 받음
        if not isinstance(skill, Skill):
            raise TypeError("skill must be a Skill type")

        if not issubclass(type(skill), DurationAttribute):
            raise TypeError("소환수는 지속시간이 있어야 함")
        
        if not issubclass(type(skill), IntervalAttribute):
            raise TypeError("소환수는 사용 간격이 있어야 함")
        
        if skill.IsBuffMult:
            mult = (skill.Owner._SummonDuration/100 + 1)
        else:
            mult = 1

        # 소환수:(스킬 이름, 공격 주기) = 스킬의 지속시간
        if hasattr(skill, 'AttackDelay'):
            self.Summons[Summon(skill=skill, interval=skill.Interval+skill.AttackDelay)] =  skill.Duration * mult - TIME_UNIT
        else:
            self.Summons[Summon(skill=skill, interval=skill.Interval)] =  skill.Duration * mult - TIME_UNIT

    def Tick(self):
        resultlogs = []
        # 소환수의 지속시간을 감소시킨다
        for summon, cool in list(self.Summons.items()):
            # 소환수의 공격 간격을 갱신함
            summonlogs = summon.Tick()
            if None !=summonlogs:
                for log in summonlogs:
                    if log is not None:
                        resultlogs.append(log)
            # 소환수의 지속시간을 갱신함
            cool.update()
            # 만약 소완수의 지속시간이 0초가 된다면
            if cool == TIME_ZERO:
                #  소환수 사라질 때 호출
                summon.Skill.EndSummon()
                del self.Summons[summon]
        return resultlogs


class Summon:
    """소환수 스킬 인스턴스
        ActiveInterval: 남은 사용 주기
    """
    def __init__(self, skill:Skill, interval:Cooldown):
        self.Skill = skill
        if hasattr(skill, 'AttackDelay'):
            self.ActiveInterval = interval
        else:
            self.ActiveInterval = Cooldown(seconds=0)
 
    def Tick(self):
        if self.ActiveInterval == TIME_ZERO:
            # 공격 간격이 일정한 경우
        
            self.ActiveInterval = deepcopy(self.Skill.Interval - TIME_UNIT)
            return self.Skill.UseSkill()
            
        else:
            self.Skill.Duration -= TIME_UNIT
            self.ActiveInterval -= TIME_UNIT
            return None

    # TODO: 소환수 사라질 때 호출할 것.
    def Timeout(self):
        pass

    def __del__(self):
        self.Timeout()
        

    
    