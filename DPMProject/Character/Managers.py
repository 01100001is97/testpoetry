from Core.Cooldown import Cooldown, TIME_UNIT, TIME_ZERO
from collections import defaultdict
from Core.ABCSkill import Skill
from Skill.Attributes import *
from copy import deepcopy


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
        self._Mercedes = value


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
        self.Cooldowns[skill] = skill().SkillCooldown

    def Tick(self):
        """모든 스킬의 쿨타임을 감소시킵니다."""
        for skill, cool in list(self.Cooldowns.items()):
            cool.update
            newCool = deepcopy(max(TIME_ZERO, cool - TIME_UNIT))

            if newCool == TIME_ZERO:
                del self.Cooldowns[skill]
            else:
                self.Cooldowns[skill] = deepcopy(Cooldown(cooldown=newCool))

    def GetRemainingCooldown(self, skill:Skill):
        """특정 스킬의 남은 쿨타임을 반환합니다."""
        if not issubclass(skill, Skill):
            raise TypeError("Skill must be a callable")
        
        return self.Cooldowns[skill]
    
    def __getitem__(self, skill):
        """특정 스킬의 남은 쿨타임을 반환합니다."""
        return self.GetRemainingCooldown(skill=skill)
    
    def __iter__(self):
        return iter(self.Cooldowns.items())
    

class BuffManager(CooldownManager):
    # TODO: 대입할때 deepcopy를 사용할 것
    def __init__(self):
        super().__init__()

    def Count(self, skill: Skill, cooldown:Cooldown):
        CooldownManager.Count(self,skill=skill, cooldown=cooldown)
        if not issubclass(skill, BuffAttribute):
            raise TypeError("버프 스킬만 관리함")
    

        
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
        
        self.Summons[Summon(skill=skill, interval=skill.Interval+skill.AttackDelay)] = skill.AttackDelay + skill.Duration
        
    def Tick(self):
        resultlogs = []
        for summon, cool in list(self.Summons.items()):
            summonlogs = summon.Tick()
            if None !=summonlogs:
                for log in summonlogs:
                    if log is not None:
                        resultlogs.append(log)
            
            cool.update()

            if cool == TIME_ZERO:
                # TODO: 소환수 사라질 때 호출
                del self.Summons[summon]
        return resultlogs


class Summon:
    """소환수 스킬 인스턴스
        ActiveInterval: 남은 사용 주기
    """
    def __init__(self, skill:Skill, interval:Cooldown):
        self.Skill = skill
        self.ActiveInterval = deepcopy(skill.AttackDelay)
 
    def Tick(self):
        
        
        if self.ActiveInterval == TIME_ZERO:
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
        

    
    