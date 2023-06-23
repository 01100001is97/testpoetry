from datetime import timedelta
from enum import Enum
from Dummy.Dummy import Dummy
from Character.ABCCharacter import ABCCharacter, CharacterStatus
from Core.Cooldown import Cooldown
from Core.ABCSkill import *
from Skill.Attributes import *
from Skill.CommonSkill import 쓸만한_샤프아이즈, 쓸만한_컴뱃오더스
from Simulator.DamageLog import DamageLog


class SimulatorEnum(Enum):
    Preset = 0
    Realtime = 1
    

class Simulator:
    """
    시뮬레이션을 수행하는 Simulator 클래스.

    Args:
        character (ABCCharacter): 시뮬레이션에 사용할 캐릭터 인스턴스.
        dummy (Dummy): 공격 대상인 더미 인스턴스.
        mode (SimulatorEnum): 시뮬레이션 모드, SimulatorEnum의 값이어야 함.

    Raises:
        TypeError: character가 ABCCharacter의 인스턴스가 아닐 경우,
                   dummy가 Dummy의 인스턴스가 아닐 경우,
                   mode가 SimulatorEnum의 인스턴스가 아닐 경우,
                   skill이 ActiveSkill의 인스턴스가 아닐 경우,
                   damage가 int가 아닐 경우.
                   
        ValueError: damage 값이 음수일 경우.
    """
    def __init__(self, character:ABCCharacter, dummy: Dummy, mode: SimulatorEnum, petbuff:list[Skill]):
        self.Character = character
        self.DummyTarget = dummy
        self.SimulationTime = timedelta(seconds=0)
        self.Mode = mode
        self.petBuffList = petbuff
        self.SimulationLog = []

    @property
    def Character(self):
        """시뮬레이션 하는 캐릭터 인스턴스

        Returns:
            _type_: _description_
        """
        return self._Character

    @Character.setter
    def Character(self, character: ABCCharacter):
        if not isinstance(character, ABCCharacter):
            raise TypeError("Character must be an instance of ABC")
        self._Character = character

    @property
    def DummyTarget(self):
        """공격의 대상이 되는 허수아비

        Returns:
            _type_: _description_
        """
        return self._Dummy

    @DummyTarget.setter
    def DummyTarget(self, dummy: Dummy):
        if not isinstance(dummy, Dummy):
            raise TypeError("Dummy must be an instance of Dummy")
        self._Dummy = dummy

    @property
    def SimulationTime(self):
        """시뮬레이션을 진행할 총 시간

        Returns:
            _type_: _description_
        """
        return self._SimulationTime

    @SimulationTime.setter
    def SimulationTime(self, time: timedelta):
        if not isinstance(time, timedelta):
            raise TypeError("SimulationTime must be an instance of timedelta")
        self._SimulationTime = time

    @property
    def Mode(self):
        """시뮬레이션 모드. 모드는 총 2가지로, SimulatorEnum 을 따름

        Returns:
            _type_: _description_
        """
        return self._Mode

    @Mode.setter
    def Mode(self, mode: 'SimulatorEnum'):
        if not isinstance(mode, SimulatorEnum):
            raise TypeError("Mode must be an instance of SimulatorEnum")
        self._Mode = mode
    
    
    @property
    def Cumulative(self):
        """DPM 시뮬레이션 시 데미지 누적값

        Returns:
            _type_: _description_
        """
        return self._Cumulative

    @Cumulative.setter
    def Cumulative(self,damage:int):
        if not isinstance(damage, int):
            raise TypeError("Damage must be an instance of int")
        
        if damage < 0:
            raise ValueError("damage must positive")
        
        self._Cumulative = damage

    @property
    def NextSkill(self):
        return self._NextSkill
    
    @NextSkill.setter
    def NextSkill(self, skill):
        if not isinstance(skill, ActiveSkill):
            raise TypeError("사용할 스킬은 ActiveSkill 형태여야 함")
        self._NextSkill = skill

    def Simulate(self, duration:timedelta, skillQueue: list):
        """캐릭터와 더미를 대상으로 DPM 시뮬레이션을 수행함

        Args:
            duration (timedelta): _description_
        """
        timeUnit = timedelta(milliseconds=10)
        CurrentTime = timedelta(seconds=0)
        SkillDelay = Cooldown(seconds=0)
        SkillIndex = 0
        nextSkill = skillQueue[SkillIndex]
        SkillIndex += 1

        

        ScheduledSkillList = []

        while CurrentTime < duration:
            # 0. 캐릭터가 행동할 수 있는 상태인지 확인: 만약 연계할 수 있다면 연계 가능한 스킬 사용 가능 = 캐릭터의 정보 로딩
                # 1. 사용할 스킬을 받아옴 (Realtime 모드에서는 어떤 스킬을 사용할 수 있는지 보여주고 입력을 대기)
                # 2. 스킬을 시전 = 캐릭터의 버프, 기본 스텟 받아옴, 타겟의 디버프, 상태 받아옴, 데미지 계산
                # 3. 데미지 저장, 디버그용 기록 저장
            # 1. 예약된 스킬들 사용
            # 2. 시간 0.01초 증가
            # 3. 버프의 지속시간이 종료되면 버프를 해제함
            
            
            # 스킬 후딜 중인지 체크함
            isSkipable = False
            if self.Character.Status in [CharacterStatus.Using_Skill]:
                # TODO: 현재 사용할 스킬이 사용중인 스킬을 스킵할 수 있는지 확인(연계)
                pass
            
            # 스킬 사용 가능 조건: 캐릭터의 휴식 혹은 다음 스킬 차례가 연계 가능한 스킬
            if self.Character.Status in [CharacterStatus.Idle] or isSkipable:
                for skill in self.Character._OnPressSkillList + self.Character._KeydownSkillList:
                    if skill == nextSkill:
                        
                        nextSkill = nextSkill()
                        break
               
            
                # 스킬의 사용자, 타겟 설정
                nextSkill._Owner = self.Character
                nextSkill._Target = self.DummyTarget

                # 스킬에 후딜이 있다면, 캐릭터를 스킬 사용 중으로 변경함
                if isinstance(nextSkill, SkillDelayAttribute):
                    SkillDelay = nextSkill.AttackDelay
                    self.Character.Status = CharacterStatus.Using_Skill

                # 컴뱃오더스가 사용중이라면 스킬에 적용
                if issubclass(type(nextSkill), CombatOrdersAttribute):    
                    nextSkill.ApplyCombat(isOriginal = 쓸만한_컴뱃오더스 not in self.petBuffList)
                    pass

                # 스킬 스케쥴 리스트에 적용
                ScheduledSkillList.append(nextSkill)

            # 스케쥴링 된 스킬을 사용하고, 만약 스킬이 완료되면 리스트에서 삭제함
            for i in range(len(ScheduledSkillList)-1, -1, -1):
                logs = ScheduledSkillList[i].UseSkill()
                for log in logs:
                    if log is not None:
                        log.Timestamp = CurrentTime
                        print(log)
                        self.SimulationLog += logs

                #print(damage)
                if ScheduledSkillList[i].Done:
                    del ScheduledSkillList[i]
            
            #   버프?
            
            ## 스킬 사용 완료 후 정리 ## -----------------------
            # 시간 경과, 다음 사용 스킬 받아옴
            CurrentTime += timeUnit
            SkillDelay.update()
            if SkillDelay == timedelta(milliseconds=0):
                self.Character.Status = CharacterStatus.Idle
            if isinstance(nextSkill, Skill):
                nextSkill = skillQueue[SkillIndex]
                SkillIndex += 1
                