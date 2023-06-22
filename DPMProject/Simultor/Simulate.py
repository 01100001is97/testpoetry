import time
from datetime import timedelta
from enum import Enum
from Dummy import Dummy
from Character.ABCCharacter import ABCCharacter


class SimulatorEnum(Enum):
    Preset = 0
    Realtime = 1
    

class Simulator:
    def __init__(self, character:ABCCharacter, dummy: Dummy, mode: SimulatorEnum):
        self.Character = character
        self.Dummy = dummy
        self.SimulationTime = timedelta(seconds=0)
        self.Mode = mode

    @property
    def Character(self):
        return self._Character

    @Character.setter
    def Character(self, character: ABCCharacter):
        if not isinstance(character, ABCCharacter):
            raise TypeError("Character must be an instance of ABC")
        self._Character = character

    @property
    def Dummy(self):
        return self._Dummy

    @Dummy.setter
    def Dummy(self, dummy: 'Dummy'):
        if not isinstance(dummy, Dummy):
            raise TypeError("Dummy must be an instance of Dummy")
        self._Dummy = dummy

    @property
    def SimulationTime(self):
        return self._SimulationTime

    @SimulationTime.setter
    def SimulationTime(self, time: timedelta):
        if not isinstance(time, timedelta):
            raise TypeError("SimulationTime must be an instance of timedelta")
        self._SimulationTime = time

    @property
    def Mode(self):
        return self._Mode

    @Mode.setter
    def Mode(self, mode: 'SimulatorEnum'):
        if not isinstance(mode, SimulatorEnum):
            raise TypeError("Mode must be an instance of SimulatorEnum")
        self._Mode = mode
    
    
    @property
    def Cumulative(self): return self._Cumulative

    @Cumulative.setter
    def Cumulative(self,damage:int):
        if not isinstance(damage, int):
            raise TypeError("Damage must be an instance of int")
        
        if damage < 0:
            raise ValueError("damage must positive")
        
        self._Cumulative = damage


    def Simulate(self, duration:timedelta):
        instanceTime = timedelta(seconds=0)
        while instanceTime < duration:
            
            # 0. 캐릭터가 행동할 수 있는 상태인지 확인: 만약 연계할 수 있다면 연계 가능한 스킬 사용 가능 = 캐릭터의 정보 로딩
                # 1. 사용할 스킬을 받아옴 (Realtime 모드에서는 어떤 스킬을 사용할 수 있는지 보여주고 입력을 대기)
                # 2. 스킬을 시전 = 캐릭터의 버프, 기본 스텟 받아옴, 타겟의 디버프, 상태 받아옴, 데미지 계산
                # 3. 데미지 저장, 디버그용 기록 저장
            # 1. 예약된 스킬들 사용
            # 2. 시간 0.01초 증가
            # 3. 버프의 지속시간이 종료되면 버프를 해제함

            
            
            # 시간 경과
            self.SimulationTime += timedelta(milliseconds=10)
            