import time
from datetime import timedelta
from enum import Enum

class SimulatorEnum(Enum):
    Preset = 0
    



class Simulator:
    def __init__(self, character, dummy, mode):
        self.character = character
        self.dummy = dummy
        self.time_passed = 0
        self.mode = 

    def simulate(self, duration):
        # 주어진 시간동안 시뮬레이션을 진행
        end_time = self.time_passed + duration
        while self.time_passed < end_time:
            # 캐릭터가 사용할 수 있는 스킬을 가져옴
            skill = self.character.get_usable_skill()
            # 스킬을 사용할 수 있으면 사용
            if skill:
                self.character.use_skill(skill, self.dummy)
            # 시간 경과
            self.time_passed += 1
            # 실제 시간으로 1초 대기 (생략해도 됨)
            time.sleep(1)
